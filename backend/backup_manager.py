#!/usr/bin/env python3
"""
Automated Database Backup System for JAC Learning Platform
Creates timestamped backups, manages retention policy, and provides restore functionality
"""

import os
import sys
import shutil
import sqlite3
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import hashlib

class DatabaseBackupManager:
    """Manages automated database backups with retention policy"""
    
    def __init__(self, db_path="/workspace/backend/db.sqlite3", backup_dir="/workspace/backend/backups"):
        self.db_path = Path(db_path)
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.max_backups = 5
        
    def create_backup(self, description=""):
        """Create a timestamped backup of the database"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"db_backup_{timestamp}"
        backup_path = self.backup_dir / f"{backup_name}.sqlite3"
        
        try:
            # Create backup using SQLite's backup API
            with sqlite3.connect(self.db_path) as source:
                with sqlite3.connect(backup_path) as backup:
                    source.backup(backup)
            
            # Calculate backup file hash for integrity verification
            backup_hash = self._calculate_file_hash(backup_path)
            
            # Create backup metadata
            metadata = {
                "backup_name": backup_name,
                "timestamp": timestamp,
                "description": description,
                "original_db_path": str(self.db_path),
                "backup_path": str(backup_path),
                "file_hash": backup_hash,
                "file_size": backup_path.stat().st_size,
                "created_at": datetime.now().isoformat()
            }
            
            # Save metadata
            metadata_path = self.backup_dir / f"{backup_name}_metadata.json"
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"✅ Database backup created successfully:")
            print(f"   File: {backup_path}")
            print(f"   Size: {backup_path.stat().st_size:,} bytes")
            print(f"   Hash: {backup_hash[:16]}...")
            print(f"   Description: {description or 'Automated backup'}")
            
            # Clean up old backups
            self._cleanup_old_backups()
            
            return backup_path, metadata
            
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return None, None
    
    def list_backups(self):
        """List all available backups with metadata"""
        backups = []
        metadata_files = list(self.backup_dir.glob("*_metadata.json"))
        
        for metadata_file in metadata_files:
            try:
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                    backups.append(metadata)
            except Exception as e:
                print(f"⚠️ Error reading metadata for {metadata_file}: {e}")
        
        # Sort by timestamp (newest first)
        backups.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return backups
    
    def restore_backup(self, backup_name=None, backup_path=None, confirm=True):
        """Restore database from a backup"""
        if backup_path:
            backup_path = Path(backup_path)
        elif backup_name:
            backup_path = self.backup_dir / f"{backup_name}.sqlite3"
        else:
            print("❌ Either backup_name or backup_path must be specified")
            return False
        
        if not backup_path.exists():
            print(f"❌ Backup file not found: {backup_path}")
            return False
        
        # Verify backup integrity
        if not self._verify_backup_integrity(backup_path):
            print(f"❌ Backup integrity check failed: {backup_path}")
            return False
        
        if confirm:
            response = input(f"⚠️ This will restore database from backup: {backup_path.name}\n")
            response = input("Are you sure? Type 'yes' to confirm: ")
            if response.lower() != 'yes':
                print("Restore cancelled.")
                return False
        
        try:
            # Create emergency backup of current database before restore
            if self.db_path.exists():
                emergency_backup = self.create_backup("Emergency backup before restore")
                print(f"📦 Emergency backup created: {emergency_backup[0].name}")
            
            # Stop Django server if running (optional)
            self._stop_django_server()
            
            # Create backup of current database
            current_backup = None
            if self.db_path.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                current_backup = self.backup_dir / f"pre_restore_backup_{timestamp}.sqlite3"
                shutil.copy2(self.db_path, current_backup)
                print(f"📦 Current database backed up as: {current_backup.name}")
            
            # Restore from backup
            shutil.copy2(backup_path, self.db_path)
            print(f"✅ Database restored successfully from: {backup_path}")
            
            # Verify restored database
            if self._verify_database_integrity():
                print("✅ Database integrity verified after restore")
            else:
                print("⚠️ Database integrity check failed after restore")
            
            return True
            
        except Exception as e:
            print(f"❌ Restore failed: {e}")
            return False
    
    def verify_backups(self):
        """Verify integrity of all backups"""
        backups = self.list_backups()
        print("🔍 Verifying backup integrity...")
        print("-" * 60)
        
        for backup in backups:
            backup_path = Path(backup['backup_path'])
            backup_name = backup['backup_name']
            
            if backup_path.exists():
                # Check file hash
                current_hash = self._calculate_file_hash(backup_path)
                stored_hash = backup.get('file_hash', '')
                
                if current_hash == stored_hash:
                    print(f"✅ {backup_name}: Integrity verified")
                else:
                    print(f"❌ {backup_name}: Hash mismatch!")
                    print(f"   Expected: {stored_hash[:16]}...")
                    print(f"   Actual:   {current_hash[:16]}...")
            else:
                print(f"⚠️ {backup_name}: Backup file not found")
    
    def get_backup_info(self, backup_name):
        """Get detailed information about a specific backup"""
        metadata_files = list(self.backup_dir.glob(f"{backup_name}_metadata.json"))
        
        if not metadata_files:
            print(f"❌ Backup metadata not found: {backup_name}")
            return None
        
        try:
            with open(metadata_files[0], 'r') as f:
                metadata = json.load(f)
                
            print(f"📋 Backup Information: {backup_name}")
            print("-" * 50)
            print(f"Created: {metadata['created_at']}")
            print(f"Description: {metadata.get('description', 'N/A')}")
            print(f"File: {metadata['backup_path']}")
            print(f"Size: {metadata['file_size']:,} bytes")
            print(f"Hash: {metadata['file_hash']}")
            
            return metadata
        except Exception as e:
            print(f"❌ Error reading backup info: {e}")
            return None
    
    def _calculate_file_hash(self, file_path):
        """Calculate SHA256 hash of a file"""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    
    def _verify_backup_integrity(self, backup_path):
        """Verify backup file integrity"""
        try:
            # Try to open and query the database
            with sqlite3.connect(backup_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                
                # Basic integrity check
                cursor.execute("PRAGMA integrity_check;")
                result = cursor.fetchone()
                
                return result[0] == "ok"
        except Exception:
            return False
    
    def _verify_database_integrity(self):
        """Verify current database integrity"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA integrity_check;")
                result = cursor.fetchone()
                return result[0] == "ok"
        except Exception:
            return False
    
    def _cleanup_old_backups(self):
        """Remove old backups beyond retention policy"""
        backups = self.list_backups()
        
        if len(backups) > self.max_backups:
            # Sort by timestamp (oldest first)
            backups.sort(key=lambda x: x['timestamp'])
            backups_to_remove = backups[:-self.max_backups]
            
            for backup in backups_to_remove:
                try:
                    # Remove backup file
                    backup_path = Path(backup['backup_path'])
                    if backup_path.exists():
                        backup_path.unlink()
                    
                    # Remove metadata file
                    metadata_path = Path(backup['backup_path']).parent / f"{backup['backup_name']}_metadata.json"
                    if metadata_path.exists():
                        metadata_path.unlink()
                    
                    print(f"🗑️ Removed old backup: {backup['backup_name']}")
                except Exception as e:
                    print(f"⚠️ Error removing backup {backup['backup_name']}: {e}")
    
    def _stop_django_server(self):
        """Stop Django server if running (optional safety measure)"""
        try:
            # Check if Django server is running
            result = subprocess.run(['pgrep', '-f', 'manage.py runserver'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("🛑 Django server detected. Consider stopping it before restore.")
                print("   Run: pkill -f 'manage.py runserver'")
        except Exception:
            pass  # pgrep might not be available
    
    def create_pre_migration_backup(self):
        """Create backup specifically for pre-migration hook"""
        return self.create_backup("Pre-migration backup")


def pre_migration_backup():
    """Hook function for Django migrations"""
    backup_manager = DatabaseBackupManager()
    print("🔄 Creating pre-migration backup...")
    backup, metadata = backup_manager.create_pre_migration_backup()
    if backup:
        print("✅ Pre-migration backup created successfully")
        return True
    else:
        print("❌ Pre-migration backup failed")
        return False


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="JAC Learning Platform Database Backup Manager")
    parser.add_argument('--db-path', default='/workspace/backend/db.sqlite3', 
                       help='Path to database file')
    parser.add_argument('--backup-dir', default='/workspace/backend/backups',
                       help='Directory for backup files')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create backup
    backup_parser = subparsers.add_parser('backup', help='Create database backup')
    backup_parser.add_argument('--description', default='', help='Backup description')
    
    # List backups
    subparsers.add_parser('list', help='List all backups')
    
    # Restore backup
    restore_parser = subparsers.add_parser('restore', help='Restore database from backup')
    restore_parser.add_argument('--name', help='Backup name to restore')
    restore_parser.add_argument('--path', help='Path to backup file')
    restore_parser.add_argument('--no-confirm', action='store_true', help='Skip confirmation')
    
    # Verify backups
    subparsers.add_parser('verify', help='Verify backup integrity')
    
    # Get backup info
    info_parser = subparsers.add_parser('info', help='Get backup information')
    info_parser.add_argument('name', help='Backup name')
    
    args = parser.parse_args()
    
    backup_manager = DatabaseBackupManager(args.db_path, args.backup_dir)
    
    if args.command == 'backup':
        backup_manager.create_backup(args.description)
    elif args.command == 'list':
        backups = backup_manager.list_backups()
        if backups:
            print("📦 Available Backups:")
            print("-" * 80)
            for backup in backups:
                print(f"{backup['backup_name']} | {backup['created_at'][:19]} | {backup['file_size']:,} bytes | {backup.get('description', 'N/A')}")
        else:
            print("No backups found.")
    elif args.command == 'restore':
        if not args.name and not args.path:
            print("❌ Either --name or --path must be specified")
            sys.exit(1)
        backup_manager.restore_backup(args.name, args.path, confirm=not args.no_confirm)
    elif args.command == 'verify':
        backup_manager.verify_backups()
    elif args.command == 'info':
        backup_manager.get_backup_info(args.name)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Comprehensive Django Model Conflict Analyzer
Identifies all field conflicts between models and existing migrations
"""

import os
import re
import ast
from pathlib import Path

def extract_model_fields(model_file_path):
    """Extract all model fields from a Django model file"""
    try:
        with open(model_file_path, 'r') as f:
            content = f.read()
        
        # Parse the file to find class definitions
        tree = ast.parse(content)
        
        model_info = {}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                fields = {}
                field_types = {}
                
                for item in node.body:
                    if isinstance(item, ast.Assign):
                        target = item.targets[0].id if isinstance(item.targets[0], ast.Name) else None
                        if target and isinstance(item.value, ast.Call):
                            # This looks like a field definition
                            func_name = item.value.func.id if isinstance(item.value.func, ast.Name) else None
                            
                            # Get field arguments
                            args = {}
                            for kw in item.value.keywords:
                                key = kw.arg
                                if isinstance(kw.value, ast.Constant):
                                    args[key] = kw.value.value
                                elif isinstance(kw.value, ast.Name):
                                    args[key] = kw.value.id
                                elif isinstance(kw.value, ast.Tuple):
                                    args[key] = [elt.value if isinstance(elt, ast.Constant) else str(elt) for elt in kw.value.elts]
                            
                            if target and func_name:
                                fields[target] = {
                                    'type': func_name,
                                    'args': args
                                }
                
                model_info[class_name] = {
                    'fields': fields,
                    'content': content
                }
        
        return model_info
    except Exception as e:
        print(f"Error parsing {model_file_path}: {e}")
        return {}

def extract_migration_fields(migration_file_path):
    """Extract fields from a migration file"""
    try:
        with open(migration_file_path, 'r') as f:
            content = f.read()
        
        # Look for CreateModel operations
        model_fields = {}
        
        # Find CreateModel operations
        pattern = r"migrations\.CreateModel\([^)]*name='([^']+)'[^)]*fields=\[([^)]+)\]"
        matches = re.findall(pattern, content, re.DOTALL)
        
        for model_name, fields_content in matches:
            fields = {}
            field_pattern = r"\('([^']+)',\s*([^,\)]+)\)"
            field_matches = re.findall(field_pattern, fields_content)
            
            for field_name, field_def in field_matches:
                fields[field_name] = field_def.strip()
            
            model_fields[model_name] = fields
        
        return model_fields
    except Exception as e:
        print(f"Error parsing {migration_file_path}: {e}")
        return {}

def analyze_all_apps():
    """Analyze all apps for model conflicts"""
    
    print("🔍 COMPREHENSIVE MODEL CONFLICT ANALYSIS")
    print("=" * 50)
    print()
    
    apps_dir = Path("/workspace/backend/apps")
    
    all_conflicts = {}
    
    for app_dir in apps_dir.iterdir():
        if not app_dir.is_dir():
            continue
            
        app_name = app_dir.name
        models_file = app_dir / "models.py"
        migrations_dir = app_dir / "migrations"
        
        if not models_file.exists():
            continue
        
        print(f"📱 Analyzing app: {app_name}")
        
        # Get model fields
        model_fields = extract_model_fields(models_file)
        
        # Get migration fields
        migration_fields = {}
        if migrations_dir.exists():
            for migration_file in migrations_dir.glob("*.py"):
                if migration_file.name != "__init__.py":
                    fields = extract_migration_fields(migration_file)
                    migration_fields.update(fields)
        
        # Compare and find conflicts
        conflicts = []
        
        for model_name in model_fields:
            model_field_names = set(model_fields[model_name]['fields'].keys())
            
            # Check if model exists in migrations
            if model_name in migration_fields:
                migration_field_names = set(migration_fields[model_name].keys())
                
                # Find differences
                added_fields = model_field_names - migration_field_names
                removed_fields = migration_field_names - model_field_names
                common_fields = model_field_names & migration_field_names
                
                if added_fields or removed_fields:
                    conflicts.append({
                        'model': model_name,
                        'added_fields': list(added_fields),
                        'removed_fields': list(removed_fields),
                        'common_fields': list(common_fields),
                        'model_fields': model_fields[model_name]['fields'],
                        'migration_fields': migration_fields[model_name]
                    })
        
        if conflicts:
            all_conflicts[app_name] = conflicts
            print(f"  ⚠️  Found {len(conflicts)} conflicts")
        else:
            print(f"  ✅ No conflicts found")
        
        print()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 CONFLICT SUMMARY")
    print("=" * 50)
    
    total_conflicts = 0
    for app_name, conflicts in all_conflicts.items():
        total_conflicts += len(conflicts)
        print(f"\n📱 {app_name.upper()}:")
        for conflict in conflicts:
            print(f"  🔧 {conflict['model']}:")
            if conflict['added_fields']:
                print(f"    + Missing in migration: {', '.join(conflict['added_fields'])}")
            if conflict['removed_fields']:
                print(f"    - Extra in migration: {', '.join(conflict['removed_fields'])}")
    
    print(f"\n🎯 TOTAL CONFLICTS FOUND: {total_conflicts}")
    
    # Generate migration fixes
    if all_conflicts:
        print("\n🛠️  GENERATING MIGRATION FIXES...")
        generate_migration_fixes(all_conflicts)
    
    return all_conflicts

def generate_migration_fixes(conflicts):
    """Generate migration fix files"""
    
    for app_name, app_conflicts in conflicts.items():
        app_dir = Path(f"/workspace/backend/apps/{app_name}")
        migrations_dir = app_dir / "migrations"
        
        if not migrations_dir.exists():
            continue
        
        # Find the highest existing migration number
        existing_migrations = list(migrations_dir.glob("*.py"))
        existing_migrations = [f for f in existing_migrations if f.name != "__init__.py"]
        
        if existing_migrations:
            # Sort by number
            existing_migrations.sort()
            last_migration = existing_migrations[-1]
            last_num = int(re.search(r'(\d+)', last_migration.stem).group(1))
            next_num = last_num + 1
        else:
            next_num = 2  # Skip 0001 as that's initial
        
        # Generate migration content
        migration_content = generate_migration_content(app_conflicts)
        
        # Write migration file
        migration_file = migrations_dir / f"{next_num:04d}_fix_field_conflicts.py"
        with open(migration_file, 'w') as f:
            f.write(migration_content)
        
        print(f"  ✅ Created: {migration_file}")

def generate_migration_content(conflicts):
    """Generate the content for a migration file"""
    
    content = '''# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

# Generated migration to fix field conflicts

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
'''

    # Add dependencies for previous migrations
    content += "    ]\n\n    operations = [\n"
    
    for conflict in conflicts:
        model_name = conflict['model']
        
        # Handle renamed fields
        if conflict['added_fields'] and conflict['removed_fields']:
            # This might be a rename
            for old_field in conflict['removed_fields']:
                for new_field in conflict['added_fields']:
                    content += f'''        migrations.RenameField(
            model_name='{model_name.lower()}',
            old_name='{old_field}',
            new_name='{new_field}',
        ),
'''
        
        # Handle added fields
        for field_name in conflict['added_fields']:
            if field_name in conflict['model_fields']:
                field_info = conflict['model_fields'][field_name]
                field_type = field_info['type']
                
                content += f'''        migrations.AddField(
            model_name='{model_name.lower()}',
            name='{field_name}',
            field=models.{field_type}(default=0),  # Set appropriate defaults
        ),
'''
        
        # Handle removed fields
        for field_name in conflict['removed_fields']:
            content += f'''        migrations.RemoveField(
            model_name='{model_name.lower()}',
            name='{field_name}',
        ),
'''
    
    content += "    ]\n"
    content += "}\n"
    
    return content

if __name__ == '__main__':
    conflicts = analyze_all_apps()
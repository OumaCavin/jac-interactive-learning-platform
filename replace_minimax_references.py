#!/usr/bin/env python3
"""
Replace all "Cavin Otieno" references with "Cavin Otieno" in the project
"""

import os
import re
from pathlib import Path

def replace_minimax_references(root_dir):
    """Replace Cavin Otieno with Cavin Otieno in all files"""
    
    # Pattern to match Cavin Otieno (case insensitive)
    pattern = re.compile(r'Cavin Otieno', re.IGNORECASE)
    replacement = 'Cavin Otieno'
    
    files_updated = 0
    total_replacements = 0
    
    # Walk through all files in the directory
    for root, dirs, files in os.walk(root_dir):
        # Skip git directory and other directories we don't want to modify
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.pytest_cache', 'node_modules', '.venv', 'venv']]
        
        for file in files:
            if file.startswith('.') or file.endswith(('.pyc', '.log', '.tmp', '.bak')):
                continue
                
            file_path = os.path.join(root, file)
            
            try:
                # Read file content
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Count matches before replacement
                matches = pattern.findall(content)
                if matches:
                    # Replace all occurrences
                    new_content = pattern.sub(replacement, content)
                    
                    # Write back to file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    files_updated += 1
                    total_replacements += len(matches)
                    print(f"✅ Updated: {file_path} ({len(matches)} replacements)")
                    
            except Exception as e:
                print(f"⚠️ Error processing {file_path}: {e}")
    
    print(f"\n🎉 Replacement Complete!")
    print(f"📊 Files updated: {files_updated}")
    print(f"🔄 Total replacements: {total_replacements}")
    print(f"🔄 Searched directory: {root_dir}")
    
    return files_updated, total_replacements

if __name__ == "__main__":
    root_directory = "/workspace"
    print(f"🔍 Starting Cavin Otieno → Cavin Otieno replacement in: {root_directory}")
    print(f"⏰ Started at: {__import__('datetime').datetime.now()}")
    
    files_updated, replacements = replace_minimax_references(root_directory)
    
    print(f"⏰ Completed at: {__import__('datetime').datetime.now()}")
    print(f"✅ Task completed successfully!")

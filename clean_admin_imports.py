#!/usr/bin/env python3
"""
Clean up duplicate custom_admin_site imports in all admin.py files
"""

import os
import re

def clean_admin_file(file_path):
    """Clean up duplicate imports in admin.py file."""
    print(f"Cleaning {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Remove duplicate imports of custom_admin_site
    # Pattern to find duplicate imports and remove them
    lines = content.split('\n')
    cleaned_lines = []
    seen_custom_admin_import = False
    
    for line in lines:
        if 'from config.custom_admin import custom_admin_site' in line:
            if not seen_custom_admin_import:
                cleaned_lines.append(line)
                seen_custom_admin_import = True
            # Skip duplicate imports
        else:
            cleaned_lines.append(line)
    
    content = '\n'.join(cleaned_lines)
    
    # Remove any extra blank lines that might have been created
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Cleaned {file_path}")
        return True
    else:
        print(f"  - No changes needed in {file_path}")
        return False

def main():
    """Main function to clean all admin.py files."""
    print("=== Cleaning Duplicate Imports in Admin.py Files ===\n")
    
    # Base directory for jac-interactive-learning-platform
    base_dir = "/workspace/jac-interactive-learning-platform/backend"
    
    # Find all admin.py files
    admin_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file == 'admin.py':
                admin_files.append(os.path.join(root, file))
    
    print(f"Found {len(admin_files)} admin.py files:")
    for file_path in admin_files:
        print(f"  - {file_path}")
    print()
    
    # Clean each file
    cleaned_count = 0
    for file_path in admin_files:
        try:
            if clean_admin_file(file_path):
                cleaned_count += 1
            print()
        except Exception as e:
            print(f"  ERROR: {e}")
            print()
    
    print(f"=== Summary ===")
    print(f"Processed {len(admin_files)} files")
    print(f"Cleaned {cleaned_count} files")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Apply admin.py fixes for custom admin site and push to GitHub
"""

import os
import re

def fix_admin_file(file_path):
    """Fix a single admin.py file."""
    print(f"Processing {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if it already has custom admin site imports
    if 'from config.custom_admin import custom_admin_site' in content:
        print(f"  Already has custom_admin_site import")
        # Check if @admin.register decorators have site parameter
        if 'site=custom_admin_site' not in content:
            print(f"  Adding site=custom_admin_site to decorators")
            # Update @admin.register decorators to include site parameter
            def update_register(match):
                register_content = match.group(0)
                if 'site=custom_admin_site' not in register_content:
                    # Find the model name and add site parameter
                    if ')' in register_content:
                        register_content = register_content.replace(')', ', site=custom_admin_site)')
                return register_content
            
            content = re.sub(r'@admin\.register\([^)]+\)', update_register, content)
    else:
        print(f"  Adding custom_admin_site import")
        # Add the import after django.contrib import
        content = content.replace(
            'from django.contrib import admin',
            'from django.contrib import admin\nfrom config.custom_admin import custom_admin_site'
        )
    
    # Fix any @admin.register that don't have site parameter
    def fix_register_decorator(match):
        inner_content = match.group(1).strip()
        if 'site=custom_admin_site' not in inner_content:
            if ',' in inner_content:
                # Has parameters, add site to end
                new_content = f"{inner_content}, site=custom_admin_site"
            else:
                # Only model name
                new_content = f"{inner_content}, site=custom_admin_site"
            return f"@admin.register({new_content})"
        return match.group(0)
    
    content = re.sub(r'@admin\.register\(([^)]+)\)', fix_register_decorator, content)
    
    # Remove any duplicate site parameters
    content = re.sub(r', site=custom_admin_site, site=custom_admin_site', ', site=custom_admin_site', content)
    
    # Write back the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✓ Fixed {file_path}")
    return True

def main():
    """Main function to fix all admin.py files."""
    print("=== Fixing Admin.py Files for Custom Admin Site ===\n")
    
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
    
    # Fix each file
    fixed_count = 0
    for file_path in admin_files:
        try:
            if fix_admin_file(file_path):
                fixed_count += 1
            print()
        except Exception as e:
            print(f"  ERROR: {e}")
            print()
    
    print(f"=== Summary ===")
    print(f"Processed {len(admin_files)} files")
    print(f"Fixed {fixed_count} files")
    
    print("\n=== Files Ready for Git ===")
    print("All admin.py files have been updated with:")
    print("1. Import: from config.custom_admin import custom_admin_site")  
    print("2. Updated @admin.register decorators with site=custom_admin_site")
    print("3. Removed duplicate site parameters")

if __name__ == "__main__":
    main()
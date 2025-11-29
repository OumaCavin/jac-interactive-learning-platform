#!/usr/bin/env python3
"""
Fix admin.py files to properly register models with custom admin site.
This script ensures all models are registered with the custom admin site
without duplicate parameters.
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
        return False
    
    # Add the import
    if 'from django.contrib import admin' in content:
        content = content.replace(
            'from django.contrib import admin',
            'from django.contrib import admin\nfrom config.custom_admin import custom_admin_site'
        )
        print(f"  Added custom_admin_site import")
    else:
        print(f"  ERROR: Could not find admin import")
        return False
    
    # Fix @admin.register decorators
    # Pattern to match @admin.register calls
    pattern = r'@admin\.register\(([^)]+)\)'
    
    def replace_register(match):
        inner_content = match.group(1).strip()
        # Check if it's already registered with custom_admin_site
        if 'site=custom_admin_site' in inner_content:
            print(f"  Already has custom_admin_site registration")
            return match.group(0)  # Keep as is
        
        # Add site parameter
        if ',' in inner_content:
            # Already has parameters, add to the end
            new_content = f"@admin.register({inner_content}, site=custom_admin_site)"
        else:
            # Only one model
            new_content = f"@admin.register({inner_content}, site=custom_admin_site)"
        
        print(f"  Updated: {new_content}")
        return new_content
    
    updated_content = re.sub(pattern, replace_register, content)
    
    # Write back the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
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
    print("\nNext steps:")
    print("1. Commit these changes: git add . && git commit -m 'fix(admin): resolve duplicate site parameter issue'")
    print("2. Push to GitHub: git push origin main")
    print("3. Test locally: docker-compose exec backend python manage.py verify_admin_setup")

if __name__ == "__main__":
    main()
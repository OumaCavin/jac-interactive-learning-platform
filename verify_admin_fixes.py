#!/usr/bin/env python3
"""
Verification script to confirm admin.py fixes are properly applied
"""

import os
import re

def verify_admin_file(file_path):
    """Verify a single admin.py file has correct configuration."""
    print(f"Verifying {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for required import
        has_import = 'from config.custom_admin import custom_admin_site' in content
        if not has_import:
            print(f"  ❌ Missing custom_admin_site import")
            return False
        
        # Check for @admin.register decorators with site parameter
        register_pattern = r'@admin\.register\([^)]+\)'
        decorators = re.findall(register_pattern, content)
        
        if not decorators:
            print(f"  ❌ No @admin.register decorators found")
            return False
        
        # Check all decorators have site parameter
        missing_site = []
        for decorator in decorators:
            if 'site=custom_admin_site' not in decorator:
                missing_site.append(decorator)
        
        if missing_site:
            print(f"  ❌ {len(missing_site)} decorators missing site parameter:")
            for decorator in missing_site:
                print(f"    - {decorator}")
            return False
        
        # Check for duplicate imports
        import_count = content.count('from config.custom_admin import custom_admin_site')
        if import_count > 1:
            print(f"  ❌ Duplicate imports found ({import_count} imports)")
            return False
        
        # Check for duplicate parameters
        duplicate_params = re.search(r'site=custom_admin_site,\s*site=custom_admin_site', content)
        if duplicate_params:
            print(f"  ❌ Duplicate site parameters found")
            return False
        
        print(f"  ✅ Properly configured")
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    """Main verification function."""
    print("=== Verifying Admin.py Fixes ===\n")
    
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
    
    # Verify each file
    verified_count = 0
    total_decorators = 0
    
    for file_path in admin_files:
        if verify_admin_file(file_path):
            verified_count += 1
            
            # Count decorators in this file
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                decorators = re.findall(r'@admin\.register\([^)]+\)', content)
                total_decorators += len(decorators)
            except:
                pass
        
        print()
    
    print(f"=== Verification Summary ===")
    print(f"Files verified: {verified_count}/{len(admin_files)}")
    print(f"Total @admin.register decorators: {total_decorators}")
    
    if verified_count == len(admin_files):
        print("🎉 ALL FILES PROPERLY CONFIGURED!")
        print("\n✅ Admin access issue should now be resolved!")
        print("🚀 Ready for testing at http://localhost:8000/admin/")
    else:
        print("❌ Some files still need fixing")

if __name__ == "__main__":
    main()
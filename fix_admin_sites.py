#!/usr/bin/env python3
"""
Script to fix all admin.py files to use the custom admin site
"""

import os
import re

def fix_admin_file(file_path):
    """Fix an admin.py file to use custom admin site"""
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Add import for custom admin site
    if 'from config.custom_admin import custom_admin_site' not in content:
        # Find the last import statement and add our import
        lines = content.split('\n')
        insert_index = -1
        for i, line in enumerate(lines):
            if line.strip().startswith('from') or line.strip().startswith('import'):
                insert_index = i
        
        if insert_index >= 0:
            lines.insert(insert_index + 1, 'from config.custom_admin import custom_admin_site')
            content = '\n'.join(lines)
    
    # Replace @admin.register with custom site
    content = re.sub(
        r'@admin\.register\(([^)]+)\)',
        r'@admin.register(\1, site=custom_admin_site)',
        content
    )
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Fixed: {file_path}")

def main():
    """Fix all admin.py files in apps"""
    
    admin_files = [
        '/workspace/backend/apps/assessments/admin.py',
        '/workspace/backend/apps/collaboration/admin.py', 
        '/workspace/backend/apps/content/admin.py',
        '/workspace/backend/apps/gamification/admin.py',
        '/workspace/backend/apps/jac_execution/admin.py',
        '/workspace/backend/apps/knowledge_graph/admin.py',
        '/workspace/backend/apps/learning/admin.py',
        '/workspace/backend/apps/users/admin.py',
        '/workspace/backend/search/admin.py',
    ]
    
    print("🔧 Fixing admin.py files to use custom admin site...")
    print("=" * 60)
    
    for file_path in admin_files:
        if os.path.exists(file_path):
            fix_admin_file(file_path)
        else:
            print(f"⚠️  File not found: {file_path}")
    
    print("\n🎉 All admin files fixed!")

if __name__ == "__main__":
    main()
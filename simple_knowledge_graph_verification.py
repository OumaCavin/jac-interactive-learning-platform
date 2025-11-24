#!/usr/bin/env python3
"""
Simple verification of Knowledge Graph app implementation.
"""

import os

def check_file_exists(file_path, description):
    """Check if a file exists and get its info."""
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        print(f"✅ {description}: {file_path} ({size:,} bytes)")
        return True
    else:
        print(f"❌ {description}: {file_path} - NOT FOUND")
        return False

def check_python_syntax(file_path):
    """Check Python syntax of a file."""
    try:
        with open(file_path, 'r') as f:
            code = f.read()
        compile(code, file_path, 'exec')
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error in {file_path}: {e}")
        return False
    except Exception as e:
        print(f"⚠️  Could not check {file_path}: {e}")
        return True

def main():
    print("Knowledge Graph App - Simple Verification")
    print("=" * 50)
    
    app_path = '/workspace/backend/apps/knowledge_graph'
    
    # Check essential files
    files_to_check = {
        f'{app_path}/__init__.py': 'App initialization',
        f'{app_path}/models.py': 'Database models',
        f'{app_path}/views.py': 'API views',
        f'{app_path}/urls.py': 'URL routing',
        f'{app_path}/admin.py': 'Admin interface',
        f'{app_path}/serializers.py': 'DRF serializers',
        f'{app_path}/apps.py': 'Django app config',
        f'{app_path}/services/graph_service.py': 'Graph service',
        f'{app_path}/migrations/0001_initial.py': 'Database migration',
    }
    
    found_files = 0
    total_files = len(files_to_check)
    
    for file_path, description in files_to_check.items():
        if check_file_exists(file_path, description):
            found_files += 1
        
        # Check syntax for Python files
        if file_path.endswith('.py'):
            check_python_syntax(file_path)
    
    print("\n" + "=" * 50)
    print(f"Files Found: {found_files}/{total_files} ({found_files/total_files*100:.1f}%)")
    
    if found_files == 2:  # Only __init__.py and apps.py
        print("\n🔴 KNOWLEDGE GRAPH APP: SEVERELY INCOMPLETE")
        print("❌ Only basic Django app structure present")
        print("❌ No knowledge graph functionality implemented")
        print("❌ Frontend integration will be completely broken")
        print("\n⚠️  IMMEDIATE DEVELOPMENT REQUIRED")
        return False
    elif found_files > 2:
        print("\n🟡 KNOWLEDGE GRAPH APP: PARTIALLY IMPLEMENTED")
        print("⚠️  Some functionality present but incomplete")
        return False
    else:
        print("\n🔴 KNOWLEDGE GRAPH APP: NO IMPLEMENTATION")
        return False

if __name__ == "__main__":
    main()
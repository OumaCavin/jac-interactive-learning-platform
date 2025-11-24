#!/usr/bin/env python3
"""
Test curriculum API endpoints directly
"""

import requests
import json
import time

def test_curriculum_api():
    """Test the curriculum API endpoints"""
    
    base_url = "http://localhost:8000/api"
    
    # Wait for server to be ready
    print("⏳ Waiting for Django server to be ready...")
    for i in range(30):
        try:
            response = requests.get(f"{base_url}/health/", timeout=2)
            if response.status_code == 200:
                print("✅ Django server is ready!")
                break
        except:
            time.sleep(1)
    else:
        print("❌ Django server not responding after 30 seconds")
        return False
    
    # Test curriculum endpoints
    endpoints = [
        "/learning/paths/",
        "/learning/modules/",
        "/learning/lessons/",
        "/learning/assessments/"
    ]
    
    print("\n🔍 Testing curriculum API endpoints:")
    print("=" * 50)
    
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        try:
            response = requests.get(url, timeout=5)
            print(f"\n📡 {endpoint}")
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    print(f"   Records: {len(data)}")
                    if data:
                        print(f"   Sample: {data[0].get('title', 'No title')}")
                elif isinstance(data, dict):
                    print(f"   Keys: {list(data.keys())}")
                    if 'results' in data:
                        print(f"   Records: {len(data['results'])}")
                        if data['results']:
                            print(f"   Sample: {data['results'][0].get('title', 'No title')}")
            elif response.status_code == 404:
                print("   ❌ Endpoint not found")
            else:
                print(f"   ⚠️  Unexpected status: {response.text[:100]}")
                
        except requests.exceptions.ConnectionError:
            print(f"\n❌ {endpoint} - Connection failed")
        except Exception as e:
            print(f"\n⚠️  {endpoint} - Error: {e}")
    
    # Test specific JAC curriculum data
    print("\n🎯 Checking JAC curriculum data:")
    print("-" * 40)
    
    try:
        # Get learning paths and filter for JAC
        response = requests.get(f"{base_url}/learning/paths/")
        if response.status_code == 200:
            paths = response.json()
            if isinstance(paths, dict) and 'results' in paths:
                paths = paths['results']
            
            jac_paths = [p for p in paths if 'JAC' in str(p.get('title', '')).upper() or 'JAC' in str(p.get('name', '')).upper()]
            
            if jac_paths:
                print(f"✅ Found {len(jac_paths)} JAC learning paths:")
                for path in jac_paths:
                    print(f"  - {path.get('title', path.get('name', 'Unknown'))} (ID: {path.get('id')})")
                    
                    # Get modules for this path
                    path_id = path.get('id')
                    modules_response = requests.get(f"{base_url}/learning/paths/{path_id}/modules/")
                    if modules_response.status_code == 200:
                        modules = modules_response.json()
                        if isinstance(modules, dict) and 'results' in modules:
                            modules = modules['results']
                        print(f"    📚 Modules: {len(modules)}")
                        
                        # Get lessons for first module as sample
                        if modules:
                            first_module = modules[0]
                            lessons_response = requests.get(f"{base_url}/learning/modules/{first_module.get('id')}/lessons/")
                            if lessons_response.status_code == 200:
                                lessons = lessons_response.json()
                                if isinstance(lessons, dict) and 'results' in lessons:
                                    lessons = lessons['results']
                                print(f"      📝 Sample lessons: {len(lessons)}")
            else:
                print("❌ No JAC learning paths found")
        else:
            print(f"❌ Failed to fetch learning paths: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing JAC curriculum: {e}")
    
    print("\n🏁 API testing completed!")

if __name__ == "__main__":
    test_curriculum_api()
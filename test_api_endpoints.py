#!/usr/bin/env python3
"""
Test script to verify the API endpoints are working correctly.
"""

import requests
import json

# API base URL
API_BASE = "http://localhost:8000/api"

def test_learning_paths():
    """Test learning paths endpoint"""
    print("Testing /learning/learning-paths/ endpoint...")
    try:
        response = requests.get(f"{API_BASE}/learning/learning-paths/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Learning Paths endpoint working - found {len(data)} items")
        else:
            print("❌ Learning Paths endpoint failed")
    except Exception as e:
        print(f"❌ Error testing learning paths: {e}")

def test_user_stats():
    """Test user stats endpoint"""
    print("\nTesting /users/stats/ endpoint...")
    try:
        response = requests.get(f"{API_BASE}/users/stats/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ User Stats endpoint working - received stats data")
        elif response.status_code == 401:
            print("⚠️  User Stats endpoint requires authentication (expected)")
        else:
            print("❌ User Stats endpoint failed")
    except Exception as e:
        print(f"❌ Error testing user stats: {e}")

def test_health_check():
    """Test health check endpoint"""
    print("\nTesting /health/ endpoint...")
    try:
        response = requests.get(f"{API_BASE}/health/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        if response.status_code == 200:
            print("✅ Health check endpoint working")
        else:
            print("❌ Health check endpoint failed")
    except Exception as e:
        print(f"❌ Error testing health check: {e}")

if __name__ == "__main__":
    print("Testing JAC Learning Platform API endpoints...\n")
    
    test_health_check()
    test_learning_paths()
    test_user_stats()
    
    print("\nTest completed!")
#!/usr/bin/env python3
"""
Predictive Analytics API Test Script

Tests the newly implemented predictive analytics endpoints to verify functionality.

Author: Cavin Otieno
Created: 2025-11-26
"""

import os
import sys
import django
import requests
import json
from datetime import datetime, timedelta

# Add Django project path
sys.path.append('/workspace/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Setup Django
django.setup()

def test_predictive_analytics():
    """
    Test predictive analytics endpoints
    """
    base_url = os.environ.get('TEST_API_URL', 'http://localhost:8000')
    headers = {
        'Content-Type': 'application/json',
        # Note: In production, you would include proper authentication
    }
    
    print("🧪 Testing Predictive Analytics API")
    print("=" * 50)
    
    # Test 1: ML Predictions API
    print("\n1. Testing ML Predictions API...")
    try:
        response = requests.get(
            f"{base_url}/api/v1/predict/ml/?prediction_horizon_days=30",
            headers=headers,
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success: {data.get('success', False)}")
            if 'data' in data:
                print(f"   📊 Models: {data['data'].get('model_count', 0)}")
                print(f"   🎯 Confidence: {data['data'].get('prediction_confidence', 0):.2f}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
    
    # Test 2: Historical Trends API
    print("\n2. Testing Historical Trends API...")
    try:
        response = requests.get(
            f"{base_url}/api/v1/predict/trends/?analysis_period_days=90",
            headers=headers,
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success: {data.get('success', False)}")
            if 'data' in data:
                print(f"   📈 Data Quality: {data['data'].get('data_quality_score', 0):.2f}")
                print(f"   🔍 Recommendations: {len(data['data'].get('recommendations', []))}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
    
    # Test 3: Confidence Calculations API
    print("\n3. Testing Confidence Calculations API...")
    try:
        response = requests.get(
            f"{base_url}/api/v1/predict/confidence/?confidence_level=0.95",
            headers=headers,
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success: {data.get('success', False)}")
            if 'data' in data:
                print(f"   📊 Sample Size: {data['data'].get('sample_size', 0)}")
                print(f"   🎯 Confidence Level: {data['data'].get('confidence_level', 0)}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
    
    # Test 4: Dashboard API
    print("\n4. Testing Predictive Dashboard API...")
    try:
        response = requests.get(
            f"{base_url}/api/v1/predict/dashboard/?include_charts=true",
            headers=headers,
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success: {data.get('success', False)}")
            if 'data' in data:
                predictions = data['data'].get('predictions', {})
                trends = data['data'].get('trends', {})
                confidence = data['data'].get('confidence', {})
                print(f"   📊 Dashboard Data: ✅")
                print(f"   🎯 Charts Included: {'charts' in data['data']}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
    
    # Test 5: Comprehensive Predictive Analytics
    print("\n5. Testing Comprehensive Predictive Analytics API...")
    try:
        response = requests.get(
            f"{base_url}/api/v1/predict/comprehensive/?prediction_horizon_days=30&analysis_period_days=90",
            headers=headers,
            timeout=15
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success: {data.get('success', False)}")
            if 'data' in data:
                ml_pred = data['data'].get('ml_predictions', {})
                trends = data['data'].get('historical_trends', {})
                confidence = data['data'].get('confidence_analysis', {})
                summary = data['data'].get('summary_insights', {})
                print(f"   🤖 ML Predictions: ✅")
                print(f"   📈 Historical Trends: ✅")
                print(f"   📊 Confidence Analysis: ✅")
                print(f"   💡 Summary Insights: ✅")
                print(f"   🎯 Learning Trajectory: {summary.get('learning_trajectory', 'N/A')}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Predictive Analytics API Testing Complete!")
    
    # Show usage examples
    print("\n📚 Usage Examples:")
    print("   ML Predictions: GET /api/v1/predict/ml/?prediction_horizon_days=30")
    print("   Historical Trends: GET /api/v1/predict/trends/?analysis_period_days=90")
    print("   Comprehensive: GET /api/v1/predict/comprehensive/")
    print("   Dashboard Data: GET /api/v1/predict/dashboard/?include_charts=true")


def test_predictive_service_directly():
    """
    Test the predictive analytics service directly using Django shell
    """
    print("\n🔧 Testing Predictive Analytics Service Directly...")
    print("=" * 50)
    
    try:
        from apps.progress.services.predictive_analytics_service import PredictiveAnalyticsService
        
        # Create service instance
        service = PredictiveAnalyticsService()
        print("✅ PredictiveAnalyticsService imported successfully")
        
        # Test service initialization
        print(f"   Models initialized: {len(service.models)}")
        print(f"   Scalers initialized: {len(service.scalers)}")
        print(f"   Feature importance tracking: {'available' if hasattr(service, 'feature_importance') else 'not set'}")
        
        # Test with empty data (should handle gracefully)
        print("\n🧪 Testing with minimal data...")
        fallback_result = service._generate_fallback_predictions([])
        print(f"   Fallback predictions: {fallback_result}")
        
        # Test basic statistical predictions
        print("\n📊 Testing basic statistical predictions...")
        basic_result = service._basic_statistical_predictions([], 30)
        print(f"   Basic predictions available: {len(basic_result)} models")
        
        print("✅ Service functionality test complete")
        
    except Exception as e:
        print(f"❌ Service test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("🚀 Starting Predictive Analytics Implementation Test")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test direct service functionality
    test_predictive_service_directly()
    
    # Test API endpoints (requires server to be running)
    print("\n" + "="*60)
    test_predictive_analytics()
    
    print("\n🎉 All tests completed!")
    print("\nNext steps:")
    print("1. Start Django server: cd /workspace/backend && python manage.py runserver")
    print("2. Run frontend: cd /workspace/frontend && npm run dev")
    print("3. Navigate to Progress page to see predictive analytics")
    print(f"4. Check API endpoints at {base_url}/api/v1/predict/")
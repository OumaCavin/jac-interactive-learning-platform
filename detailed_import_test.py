#!/usr/bin/env python3
import os
import sys
import django

sys.path.append('/workspace/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

try:
    # Import each service individually to isolate the issue
    print("Testing individual imports...")
    
    # Test the realtime monitoring service
    from apps.progress.services.realtime_monitoring_service import RealtimeMonitoringService
    service = RealtimeMonitoringService()
    print(f"✅ RealtimeMonitoringService: {type(service)}")
    
    # Test background monitoring service  
    from apps.progress.services.background_monitoring_service import BackgroundMonitoringService
    bg_service = BackgroundMonitoringService()
    print(f"✅ BackgroundMonitoringService: {type(bg_service)}")
    
    # Test analytics service
    from apps.progress.services.analytics_service import AnalyticsService
    analytics_service = AnalyticsService()
    print(f"✅ AnalyticsService: {type(analytics_service)}")
    
    # Try importing predictive analytics
    from apps.progress.services.predictive_analytics_service import PredictiveAnalyticsService
    predictive_service = PredictiveAnalyticsService()
    print(f"✅ PredictiveAnalyticsService: {type(predictive_service)}")
    
    # Test views
    from apps.progress.views_realtime import RealTimeDashboardAPIView
    print("✅ RealTimeDashboardAPIView imported")
    
    from apps.progress.views_realtime import PerformanceAlertsAPIView
    print("✅ PerformanceAlertsAPIView imported")
    
    from apps.progress.views_realtime import PredictiveAnalyticsAPIView
    print("✅ PredictiveAnalyticsAPIView imported")
    
    print("\n🎉 All imports successful! Testing consumers...")
    
    # Now test consumers
    from apps.progress.consumers import DashboardConsumer
    print("✅ DashboardConsumer imported")
    
    from apps.progress.consumers import AlertConsumer
    print("✅ AlertConsumer imported")
    
    from apps.progress.consumers import RealtimeMetricsConsumer
    print("✅ RealtimeMetricsConsumer imported")
    
    print("\n🚀 All components imported successfully!")
    
except Exception as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()
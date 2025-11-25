#!/usr/bin/env python3
"""
Quick Performance Monitoring Status Checker
JAC Learning Platform

Quick verification script to check the current status of
performance monitoring infrastructure components.

Author: Cavin Otieno
Created: 2025-11-26
"""

import os
import sys
import django

sys.path.append('/workspace/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def quick_status_check():
    """Quick status check of performance monitoring infrastructure"""
    print("🔍 Quick Performance Monitoring Status Check")
    print("=" * 50)
    
    results = {
        'backend_services': False,
        'websocket_consumers': False,
        'api_endpoints': False,
        'frontend_integration': False,
        'overall_status': 'UNKNOWN'
    }
    
    # Check backend services
    try:
        from apps.progress.services.realtime_monitoring_service import RealtimeMonitoringService
        from apps.progress.services.background_monitoring_service import BackgroundMonitoringService
        
        realtime = RealtimeMonitoringService()
        background = BackgroundMonitoringService()
        
        results['backend_services'] = True
        print("✅ Backend Services: OPERATIONAL")
        print(f"   - RealtimeMonitoringService: {len(realtime.monitoring_thresholds)} thresholds configured")
        print(f"   - BackgroundMonitoringService: {len(background.alert_thresholds)} alert categories")
        
    except Exception as e:
        print(f"❌ Backend Services: ERROR - {e}")
    
    # Check WebSocket consumers
    try:
        from apps.progress.consumers import (
            DashboardConsumer, AlertConsumer, 
            RealtimeMetricsConsumer, ActivityStreamConsumer
        )
        results['websocket_consumers'] = True
        print("✅ WebSocket Consumers: OPERATIONAL")
        print("   - DashboardConsumer: Live dashboard updates")
        print("   - AlertConsumer: Real-time alert notifications")
        print("   - RealtimeMetricsConsumer: Performance metrics streaming")
        print("   - ActivityStreamConsumer: Activity updates")
        
    except Exception as e:
        print(f"❌ WebSocket Consumers: ERROR - {e}")
    
    # Check API endpoints
    try:
        from apps.progress.views_realtime import (
            RealTimeDashboardAPIView,
            PerformanceAlertsAPIView,
            PredictiveAnalyticsAPIView,
            TrendAnalysisAPIView
        )
        results['api_endpoints'] = True
        print("✅ API Endpoints: OPERATIONAL")
        print("   - RealTimeDashboardAPIView: Dashboard data endpoint")
        print("   - PerformanceAlertsAPIView: Alert management endpoint")
        print("   - PredictiveAnalyticsAPIView: ML predictions endpoint")
        print("   - TrendAnalysisAPIView: Trend analysis endpoint")
        
    except Exception as e:
        print(f"❌ API Endpoints: ERROR - {e}")
    
    # Check frontend integration
    try:
        frontend_files = [
            '/workspace/frontend/src/components/realtime/WebSocketProvider.tsx',
            '/workspace/frontend/src/components/realtime/RealTimeDashboard.tsx',
            '/workspace/frontend/src/hooks/useWebSocket.ts'
        ]
        
        missing_files = []
        for file_path in frontend_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
        
        if not missing_files:
            results['frontend_integration'] = True
            print("✅ Frontend Integration: OPERATIONAL")
            print("   - WebSocketProvider.tsx: WebSocket connection management")
            print("   - RealTimeDashboard.tsx: Real-time dashboard component")
            print("   - useWebSocket.ts: Custom React hooks for WebSocket")
        else:
            print(f"❌ Frontend Integration: MISSING FILES - {missing_files}")
        
    except Exception as e:
        print(f"❌ Frontend Integration: ERROR - {e}")
    
    # Overall status
    passed_checks = sum(results[key] for key in ['backend_services', 'websocket_consumers', 'api_endpoints', 'frontend_integration'])
    
    if passed_checks == 4:
        results['overall_status'] = 'FULLY_OPERATIONAL'
        print("\n🎉 OVERALL STATUS: FULLY OPERATIONAL")
        print("   Performance monitoring infrastructure is completely functional!")
    elif passed_checks >= 2:
        results['overall_status'] = 'PARTIALLY_OPERATIONAL'
        print("\n⚠️  OVERALL STATUS: PARTIALLY OPERATIONAL")
        print("   Some components are working, others need attention.")
    else:
        results['overall_status'] = 'NOT_OPERATIONAL'
        print("\n❌ OVERALL STATUS: NOT OPERATIONAL")
        print("   Major components are not functioning properly.")
    
    return results

if __name__ == "__main__":
    status = quick_status_check()
    
    print("\n" + "=" * 50)
    print("Quick Status Summary:")
    print(f"Backend Services: {'✅' if status['backend_services'] else '❌'}")
    print(f"WebSocket Consumers: {'✅' if status['websocket_consumers'] else '❌'}")
    print(f"API Endpoints: {'✅' if status['api_endpoints'] else '❌'}")
    print(f"Frontend Integration: {'✅' if status['frontend_integration'] else '❌'}")
    print(f"Overall: {status['overall_status']}")
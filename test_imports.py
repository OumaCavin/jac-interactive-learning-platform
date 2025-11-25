#!/usr/bin/env python3
import os
import sys
import django

sys.path.append('/workspace/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

try:
    from apps.progress.services.realtime_monitoring_service import RealtimeMonitoringService
    print("✅ RealtimeMonitoringService imported successfully")
except Exception as e:
    print(f"❌ Error importing RealtimeMonitoringService: {e}")

try:
    from apps.progress.services.background_monitoring_service import BackgroundMonitoringService
    print("✅ BackgroundMonitoringService imported successfully")
except Exception as e:
    print(f"❌ Error importing BackgroundMonitoringService: {e}")

try:
    from apps.progress.consumers import AlertConsumer
    print("✅ AlertConsumer imported successfully")
except Exception as e:
    print(f"❌ Error importing AlertConsumer: {e}")

try:
    from apps.progress.views_realtime import PerformanceAlertsAPIView
    print("✅ PerformanceAlertsAPIView imported successfully")
except Exception as e:
    print(f"❌ Error importing PerformanceAlertsAPIView: {e}")
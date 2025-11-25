#!/usr/bin/env python3
"""
Real-time Streaming Features Verification Script

This script verifies the implementation status of real-time streaming components:
1. WebSocket connections for live updates
2. Real-time dashboard data feeds  
3. Continuous performance monitoring background tasks

Author: Cavin Otieno
Created: 2025-11-26
"""

import os
import sys
from pathlib import Path

def check_websocket_consumers():
    """Check if WebSocket consumers are properly implemented"""
    consumers_path = Path("/workspace/backend/apps/progress/consumers.py")
    
    if not consumers_path.exists():
        return {"status": "MISSING", "details": "consumers.py file does not exist"}
    
    with open(consumers_path, 'r') as f:
        content = f.read()
    
    consumers = {
        "DashboardConsumer": "DashboardConsumer" in content,
        "AlertConsumer": "AlertConsumer" in content,
        "RealtimeMetricsConsumer": "RealtimeMetricsConsumer" in content,
        "ActivityStreamConsumer": "ActivityStreamConsumer" in content
    }
    
    missing_consumers = [name for name, exists in consumers.items() if not exists]
    
    return {
        "status": "IMPLEMENTED" if not missing_consumers else "PARTIAL",
        "details": f"Found {sum(consumers.values())}/4 consumers",
        "missing": missing_consumers,
        "consumers": consumers
    }

def check_websocket_routing():
    """Check if WebSocket routing is configured"""
    routing_path = Path("/workspace/backend/apps/progress/routing.py")
    
    if not routing_path.exists():
        return {"status": "MISSING", "details": "routing.py file does not exist"}
    
    with open(routing_path, 'r') as f:
        content = f.read()
    
    routes = {
        "/ws/dashboard/": "ws/dashboard" in content,
        "/ws/alerts/": "ws/alerts" in content,
        "/ws/metrics/": "ws/metrics" in content,
        "/ws/activity/": "ws/activity" in content
    }
    
    missing_routes = [route for route, exists in routes.items() if not exists]
    
    return {
        "status": "IMPLEMENTED" if not missing_routes else "PARTIAL",
        "details": f"Found {sum(routes.values())}/4 WebSocket routes",
        "missing": missing_routes,
        "routes": routes
    }

def check_background_monitoring():
    """Check if background monitoring service is implemented"""
    monitoring_path = Path("/workspace/backend/apps/progress/services/background_monitoring_service.py")
    command_path = Path("/workspace/backend/apps/progress/management/commands/start_monitoring.py")
    
    results = {}
    
    # Check service implementation
    if not monitoring_path.exists():
        results["service"] = {"status": "MISSING", "details": "background_monitoring_service.py does not exist"}
    else:
        with open(monitoring_path, 'r') as f:
            content = f.read()
        
        has_start_method = "start_background_monitoring" in content
        has_monitoring_loop = "_run_monitoring_loop" in content
        has_scheduling = "schedule" in content
        
        results["service"] = {
            "status": "IMPLEMENTED" if has_start_method and has_monitoring_loop else "PARTIAL",
            "details": f"Service methods: start={has_start_method}, loop={has_monitoring_loop}, scheduling={has_scheduling}",
            "has_start_method": has_start_method,
            "has_monitoring_loop": has_monitoring_loop,
            "has_scheduling": has_scheduling
        }
    
    # Check management command
    if not command_path.exists():
        results["command"] = {"status": "MISSING", "details": "start_monitoring.py does not exist"}
    else:
        results["command"] = {
            "status": "IMPLEMENTED",
            "details": "Management command exists and can start monitoring service"
        }
    
    return results

def check_frontend_integration():
    """Check if frontend has WebSocket integration"""
    frontend_path = Path("/workspace/frontend")
    
    if not frontend_path.exists():
        return {"status": "MISSING", "details": "Frontend directory does not exist"}
    
    # Check for WebSocket-related components
    websocket_patterns = ["WebSocket", "ws://", "socket", "realtime"]
    results = {}
    
    # Check Dashboard component
    dashboard_path = frontend_path / "src" / "pages" / "Dashboard.tsx"
    if dashboard_path.exists():
        with open(dashboard_path, 'r') as f:
            dashboard_content = f.read()
        
        has_websocket = any(pattern in dashboard_content for pattern in websocket_patterns)
        results["Dashboard"] = {
            "status": "HAS_WEBSOCKET" if has_websocket else "NO_WEBSOCKET",
            "details": "Dashboard component WebSocket integration"
        }
    
    # Check MainLayout component
    layout_path = frontend_path / "src" / "components" / "layout" / "MainLayout.tsx"
    if layout_path.exists():
        with open(layout_path, 'r') as f:
            layout_content = f.read()
        
        has_websocket = any(pattern in layout_content for pattern in websocket_patterns)
        results["MainLayout"] = {
            "status": "HAS_WEBSOCKET" if has_websocket else "NO_WEBSOCKET",
            "details": "MainLayout component WebSocket integration"
        }
    
    # Check for any custom WebSocket hook or service
    hook_files = list((frontend_path / "src").glob("**/*socket*")) + list((frontend_path / "src").glob("**/*realtime*"))
    results["custom_hooks"] = {
        "status": "EXISTS" if hook_files else "MISSING",
        "details": f"Found {len(hook_files)} custom WebSocket/realtime files"
    }
    
    return results

def check_main_routing_integration():
    """Check if WebSocket routing is integrated into main Django routing"""
    # This would typically be in asgi.py or routing configuration
    # For now, we'll check if there's any ASGI configuration
    
    asgi_path = Path("/workspace/backend/config/asgi.py")
    
    if not asgi_path.exists():
        return {"status": "MISSING", "details": "ASGI configuration does not exist"}
    
    with open(asgi_path, 'r') as f:
        content = f.read()
    
    has_protocol_router = "ProtocolTypeRouter" in content
    has_websocket_route = "websocket" in content.lower()
    
    return {
        "status": "IMPLEMENTED" if has_protocol_router and has_websocket_route else "PARTIAL",
        "details": f"ASGI routing: protocol_router={has_protocol_router}, websocket_route={has_websocket_route}"
    }

def main():
    """Main verification function"""
    print("🔍 Real-time Streaming Features Verification")
    print("=" * 60)
    
    results = {}
    
    # Check WebSocket Consumers
    print("\n📡 WebSocket Consumers:")
    consumers_result = check_websocket_consumers()
    print(f"   Status: {consumers_result['status']}")
    print(f"   Details: {consumers_result['details']}")
    if consumers_result.get('missing'):
        print(f"   Missing: {consumers_result['missing']}")
    results['consumers'] = consumers_result
    
    # Check WebSocket Routing
    print("\n🔗 WebSocket Routing:")
    routing_result = check_websocket_routing()
    print(f"   Status: {routing_result['status']}")
    print(f"   Details: {routing_result['details']}")
    if routing_result.get('missing'):
        print(f"   Missing: {routing_result['missing']}")
    results['routing'] = routing_result
    
    # Check Background Monitoring
    print("\n⚙️  Background Monitoring:")
    monitoring_result = check_background_monitoring()
    for component, result in monitoring_result.items():
        print(f"   {component}: {result['status']} - {result['details']}")
    results['monitoring'] = monitoring_result
    
    # Check Frontend Integration
    print("\n🖥️  Frontend Integration:")
    frontend_result = check_frontend_integration()
    for component, result in frontend_result.items():
        print(f"   {component}: {result['status']} - {result['details']}")
    results['frontend'] = frontend_result
    
    # Check Main Routing Integration
    print("\n🌐 ASGI/Routing Integration:")
    routing_integration = check_main_routing_integration()
    print(f"   Status: {routing_integration['status']}")
    print(f"   Details: {routing_integration['details']}")
    results['routing_integration'] = routing_integration
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 IMPLEMENTATION STATUS SUMMARY")
    print("=" * 60)
    
    # Check for gaps
    gaps = []
    
    if consumers_result['status'] != 'IMPLEMENTED':
        gaps.append("WebSocket Consumers")
    
    if routing_result['status'] != 'IMPLEMENTED':
        gaps.append("WebSocket Routing")
    
    if not all(r['status'] == 'IMPLEMENTED' for r in monitoring_result.values()):
        gaps.append("Background Monitoring Service")
    
    frontend_has_websocket = any(r['status'] == 'HAS_WEBSOCKET' for r in frontend_result.values())
    if not frontend_has_websocket:
        gaps.append("Frontend WebSocket Integration")
    
    if routing_integration['status'] != 'IMPLEMENTED':
        gaps.append("ASGI/Routing Integration")
    
    if gaps:
        print(f"\n❌ IMPLEMENTATION GAPS DETECTED:")
        for gap in gaps:
            print(f"   • {gap}")
        
        print(f"\n🔧 MISSING COMPONENTS NEED IMPLEMENTATION:")
        
        if not frontend_has_websocket:
            print("   • Frontend WebSocket client components")
            print("   • Real-time dashboard data feeds")
            print("   • WebSocket connection management")
        
        if routing_integration['status'] != 'IMPLEMENTED':
            print("   • ASGI application configuration")
            print("   • WebSocket routing integration")
        
        return False
    else:
        print("\n🎉 ALL REAL-TIME STREAMING FEATURES IMPLEMENTED!")
        print("\n✅ Complete Implementation Status:")
        print("   • WebSocket connections for live updates")
        print("   • Real-time dashboard data feeds")
        print("   • Continuous performance monitoring background tasks")
        
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
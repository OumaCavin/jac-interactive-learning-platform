"""
WebSocket Consumers - JAC Learning Platform

WebSocket consumers for real-time dashboard data feeds, live alerts,
and continuous performance monitoring.

Author: Cavin Otieno
Created: 2025-11-26
"""

import json
import uuid
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.utils import timezone

from .services.realtime_monitoring_service import RealtimeMonitoringService

User = get_user_model()


class DashboardConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time dashboard updates
    """
    
    async def connect(self):
        """Handle WebSocket connection"""
        self.session_id = str(uuid.uuid4())
        self.monitoring_service = RealtimeMonitoringService()
        
        # Get user from scope
        self.user = self.scope["user"]
        
        if isinstance(self.user, AnonymousUser):
            await self.close()
            return
        
        # Add user to their group
        self.room_group_name = f"user_{self.user.id}"
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        # Start monitoring session
        result = await self.monitoring_service.start_user_monitoring(
            self.user.id, 
            self.session_id
        )
        
        if result['success']:
            await self.accept()
            
            # Send connection confirmation
            await self.send(text_data=json.dumps({
                'type': 'connection_established',
                'session_id': self.session_id,
                'message': 'Dashboard monitoring started'
            }))
        else:
            await self.close()
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        if hasattr(self, 'monitoring_service') and hasattr(self, 'user'):
            # Stop monitoring session
            await self.monitoring_service.stop_user_monitoring(
                self.user.id,
                self.session_id
            )
        
        # Remove user from group
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
    
    async def receive(self, text_data):
        """Handle incoming WebSocket messages"""
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type')
            
            if message_type == 'ping':
                # Respond to ping
                await self.send(text_data=json.dumps({
                    'type': 'pong',
                    'timestamp': timezone.now().isoformat()
                }))
            
            elif message_type == 'request_update':
                # User requesting manual update
                await self._handle_manual_update_request()
            
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON received'
            }))
    
    async def send_to_user(self, event):
        """Send message to user (called by group_send)"""
        data = event['data']
        await self.send(text_data=json.dumps(data))
    
    async def _handle_manual_update_request(self):
        """Handle manual update request from user"""
        try:
            # Generate fresh dashboard data
            dashboard_data = await self._generate_dashboard_update()
            
            await self.send(text_data=json.dumps(dashboard_data))
            
        except Exception as e:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f'Failed to generate update: {str(e)}'
            }))
    
    async def _generate_dashboard_update(self) -> dict:
        """Generate fresh dashboard update data"""
        from ..services.analytics_service import AnalyticsService
        
        analytics_service = AnalyticsService()
        
        # Get current analytics
        analytics_data = await database_sync_to_async(analytics_service.generate_comprehensive_analytics)(
            user=self.user,
            analytics_type='comprehensive'
        )
        
        return {
            'type': 'dashboard_update',
            'timestamp': timezone.now().isoformat(),
            'data': analytics_data
        }


class AlertConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer specifically for alerts and notifications
    """
    
    async def connect(self):
        """Handle WebSocket connection for alerts"""
        self.session_id = str(uuid.uuid4())
        self.alert_group_name = f"alerts_{self.scope['user'].id}"
        
        # Check if user is authenticated
        if isinstance(self.scope["user"], AnonymousUser):
            await self.close()
            return
        
        # Add user to alert group
        await self.channel_layer.group_add(
            self.alert_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send initial alert status
        await self.send(text_data=json.dumps({
            'type': 'alert_connection_established',
            'session_id': self.session_id
        }))
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        await self.channel_layer.group_discard(
            self.alert_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """Handle incoming alert messages"""
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type')
            
            if message_type == 'acknowledge_alert':
                # User acknowledged an alert
                alert_id = text_data_json.get('alert_id')
                await self._acknowledge_alert(alert_id)
            
        except json.JSONDecodeError:
            pass
    
    async def send_alert_notification(self, event):
        """Send alert notification to user"""
        alert_data = event['alert']
        await self.send(text_data=json.dumps({
            'type': 'alert_notification',
            'alert': alert_data,
            'timestamp': timezone.now().isoformat()
        }))
    
    async def _acknowledge_alert(self, alert_id: str):
        """Mark alert as acknowledged"""
        try:
            from ..models import ProgressNotification
            
            # Update notification in database
            await database_sync_to_async(
                ProgressNotification.objects.filter
            )(id=alert_id, user=self.scope['user']).update(is_read=True)
            
        except Exception as e:
            print(f"Error acknowledging alert: {e}")


class RealtimeMetricsConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time performance metrics
    """
    
    async def connect(self):
        """Handle WebSocket connection for real-time metrics"""
        self.session_id = str(uuid.uuid4())
        self.metrics_group_name = f"metrics_{self.scope['user'].id}"
        
        if isinstance(self.scope["user"], AnonymousUser):
            await self.close()
            return
        
        # Add user to metrics group
        await self.channel_layer.group_add(
            self.metrics_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        await self.channel_layer.group_discard(
            self.metrics_group_name,
            self.channel_name
        )
    
    async def send_realtime_metrics(self, event):
        """Send real-time metrics update"""
        metrics_data = event['metrics']
        await self.send(text_data=json.dumps({
            'type': 'realtime_metrics',
            'metrics': metrics_data,
            'timestamp': timezone.now().isoformat()
        }))
    
    async def receive(self, text_data):
        """Handle incoming messages"""
        # Metrics consumer is primarily for receiving updates
        # User-initiated requests are handled minimally
        pass


class ActivityStreamConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for live activity streams
    """
    
    async def connect(self):
        """Handle WebSocket connection for activity streams"""
        self.session_id = str(uuid.uuid4())
        self.activity_group_name = f"activity_{self.scope['user'].id}"
        
        if isinstance(self.scope["user"], AnonymousUser):
            await self.close()
            return
        
        # Add user to activity group
        await self.channel_layer.group_add(
            self.activity_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        await self.channel_layer.group_discard(
            self.activity_group_name,
            self.channel_name
        )
    
    async def send_activity_update(self, event):
        """Send activity update to user"""
        activity_data = event['activity']
        await self.send(text_data=json.dumps({
            'type': 'activity_update',
            'activity': activity_data,
            'timestamp': timezone.now().isoformat()
        }))
    
    async def send_new_achievement(self, event):
        """Send achievement notification"""
        achievement_data = event['achievement']
        await self.send(text_data=json.dumps({
            'type': 'achievement_unlocked',
            'achievement': achievement_data,
            'timestamp': timezone.now().isoformat()
        }))
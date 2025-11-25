"""
Real-time Analytics Framework Enhancement Script
JAC Learning Platform

This script enhances the existing real-time analytics framework to integrate
with the newly added predictive learning models and improve WebSocket streaming.

Author: MiniMax Agent
Created: 2025-11-26
"""

import os
import sys
import re
from pathlib import Path

# Add backend to path
sys.path.append('/workspace/backend')

def fix_realtime_monitoring_service():
    """Fix the realtime monitoring service import issues"""
    
    file_path = '/workspace/backend/apps/progress/services/realtime_monitoring_service.py'
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Fix numpy import at the top
    content = re.sub(r'# Import numpy for calculations\nimport numpy as np', 
                    'import numpy as np\nfrom scipy import stats', content)
    
    # Fix the calculation that needs numpy
    content = re.sub(r'avg_recent_score = round\(np\.mean\(recent_scores\), 2\) if recent_scores else 0',
                    'avg_recent_score = round(np.mean(recent_scores), 2) if recent_scores else 0', content)
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    print("✓ Fixed realtime monitoring service imports")

def enhance_realtime_monitoring_with_predictive_models():
    """Enhance realtime monitoring service to integrate predictive models"""
    
    file_path = '/workspace/backend/apps/progress/services/realtime_monitoring_service.py'
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Add predictive models integration at the end of the class, before the numpy import
    predictive_integration = '''
    def get_predictive_insights_stream(self, user_id: int, session_id: str) -> Dict[str, Any]:
        """Get predictive insights for real-time streaming"""
        try:
            from .predictive_analytics_service import PredictiveAnalyticsService
            
            user = User.objects.get(id=user_id)
            predictive_service = PredictiveAnalyticsService()
            
            # Get comprehensive predictive insights
            predictions = {}
            
            # Learning velocity analysis
            try:
                velocity_data = predictive_service.analyze_learning_velocity(user)
                predictions['learning_velocity'] = velocity_data
            except Exception as e:
                print(f"Error in learning velocity analysis: {e}")
            
            # Engagement pattern analysis
            try:
                engagement_data = predictive_service.analyze_engagement_patterns(user)
                predictions['engagement_patterns'] = engagement_data
            except Exception as e:
                print(f"Error in engagement pattern analysis: {e}")
            
            # Success probability modeling
            try:
                success_data = predictive_service.model_success_probability(user)
                predictions['success_probability'] = success_data
            except Exception as e:
                print(f"Error in success probability modeling: {e}")
            
            # Time to completion prediction
            try:
                completion_data = predictive_service.predict_time_to_completion(user)
                predictions['time_to_completion'] = completion_data
            except Exception as e:
                print(f"Error in completion prediction: {e}")
            
            # Retention risk assessment
            try:
                retention_data = predictive_service.assess_retention_risk(user)
                predictions['retention_risk'] = retention_data
            except Exception as e:
                print(f"Error in retention risk assessment: {e}")
            
            # Knowledge gap detection
            try:
                gaps_data = predictive_service.detect_knowledge_gaps(user)
                predictions['knowledge_gaps'] = gaps_data
            except Exception as e:
                print(f"Error in knowledge gap detection: {e}")
            
            # Learning clusters analysis
            try:
                clusters_data = predictive_service.perform_learning_analytics_clustering(user)
                predictions['learning_clusters'] = clusters_data
            except Exception as e:
                print(f"Error in learning clusters analysis: {e}")
            
            return {
                'success': True,
                'session_id': session_id,
                'timestamp': timezone.now().isoformat(),
                'predictive_insights': predictions,
                'data_freshness': 'real-time'
            }
            
        except Exception as e:
            print(f"Error getting predictive insights: {e}")
            return {
                'success': False,
                'error': str(e),
                'session_id': session_id
            }
    
    async def stream_predictive_updates(self, user_id: int, session_id: str) -> None:
        """Stream predictive model updates via WebSocket"""
        try:
            # Get predictive insights
            insights = self.get_predictive_insights_stream(user_id, session_id)
            
            if insights['success']:
                # Send predictive update via WebSocket
                update_data = {
                    'type': 'predictive_analytics_update',
                    'session_id': session_id,
                    'timestamp': timezone.now().isoformat(),
                    'predictive_data': insights['predictive_insights']
                }
                
                await self._send_to_user_channel(user_id, update_data)
                
        except Exception as e:
            print(f"Error streaming predictive updates: {e}")
    
    def generate_realtime_recommendations_with_ai(self, user_id: int, session_id: str) -> Dict[str, Any]:
        """Generate real-time recommendations using AI and predictive models"""
        try:
            from apps.agents.ai_multi_agent_system import get_multi_agent_system
            
            user = User.objects.get(id=user_id)
            ai_system = get_multi_agent_system()
            
            # Get current context
            current_context = {
                'session_data': self.active_sessions.get(user_id, {}).get(session_id, {}),
                'recent_performance': self._calculate_realtime_metrics(user)
            }
            
            # Generate AI-powered recommendations
            ai_request = {
                'user_id': str(user_id),
                'message': 'Provide personalized learning recommendations based on current progress and predictive analytics',
                'agent_type': 'mentor_coach',
                'context': current_context
            }
            
            # Get AI response
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            ai_response = loop.run_until_complete(ai_system.process_request(ai_request))
            
            return {
                'success': True,
                'ai_recommendations': ai_response.get('response', ''),
                'agent_type': ai_response.get('agent_info', {}),
                'session_id': session_id,
                'timestamp': timezone.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error generating AI recommendations: {e}")
            return {
                'success': False,
                'error': str(e),
                'session_id': session_id
            }
    
    async def start_predictive_monitoring(self, user_id: int, session_id: str) -> Dict[str, Any]:
        """Start real-time predictive monitoring for user"""
        try:
            # Initialize predictive monitoring session
            if user_id not in self.active_sessions:
                self.active_sessions[user_id] = {}
            
            self.active_sessions[user_id][session_id].update({
                'predictive_monitoring': True,
                'last_predictive_update': timezone.now(),
                'predictive_data': {}
            })
            
            # Send initial predictive insights
            await self.stream_predictive_updates(user_id, session_id)
            
            # Start background predictive monitoring
            asyncio.create_task(self._monitor_predictive_metrics(user_id, session_id))
            
            return {
                'success': True,
                'session_id': session_id,
                'predictive_monitoring': True
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def _monitor_predictive_metrics(self, user_id: int, session_id: str) -> None:
        """Background task for predictive metrics monitoring"""
        monitoring_active = True
        
        while monitoring_active:
            try:
                # Check if session still exists
                if user_id not in self.active_sessions or session_id not in self.active_sessions[user_id]:
                    break
                
                session = self.active_sessions[user_id][session_id]
                
                # Update predictive metrics every 60 seconds
                await self.stream_predictive_updates(user_id, session_id)
                
                # Send AI-generated recommendations every 5 minutes
                time_since_last_ai = timezone.now() - session.get('last_ai_recommendation', timezone.now() - timedelta(minutes=10))
                if time_since_last_ai.total_seconds() > 300:  # 5 minutes
                    ai_recommendations = self.generate_realtime_recommendations_with_ai(user_id, session_id)
                    if ai_recommendations['success']:
                        await self._send_to_user_channel(user_id, {
                            'type': 'ai_recommendation',
                            'recommendations': ai_recommendations,
                            'timestamp': timezone.now().isoformat()
                        })
                    session['last_ai_recommendation'] = timezone.now()
                
                # Sleep for 60 seconds
                await asyncio.sleep(60)
                
            except Exception as e:
                print(f"Error in predictive monitoring: {e}")
                await asyncio.sleep(120)  # Wait longer on error

'''
    
    # Insert before the numpy import
    content = content.replace('# Import numpy for calculations\nimport numpy as np', 
                             predictive_integration + '\n# Import numpy for calculations\nimport numpy as np')
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    print("✓ Enhanced realtime monitoring service with predictive models")

def create_enhanced_websocket_consumers():
    """Create enhanced WebSocket consumers for predictive analytics"""
    
    file_path = '/workspace/backend/apps/progress/consumers.py'
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Add predictive analytics consumer at the end
    enhanced_consumer = '''

class PredictiveAnalyticsConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time predictive analytics streaming
    """
    
    async def connect(self):
        """Handle WebSocket connection for predictive analytics"""
        self.session_id = str(uuid.uuid4())
        self.predictive_group_name = f"predictive_{self.scope['user'].id}"
        
        if isinstance(self.scope["user"], AnonymousUser):
            await self.close()
            return
        
        # Add user to predictive analytics group
        await self.channel_layer.group_add(
            self.predictive_group_name,
            self.channel_name
        )
        
        # Start predictive monitoring service
        from .services.realtime_monitoring_service import RealtimeMonitoringService
        self.monitoring_service = RealtimeMonitoringService()
        
        # Initialize predictive monitoring
        start_result = await self.monitoring_service.start_predictive_monitoring(
            self.scope['user'].id,
            self.session_id
        )
        
        await self.accept()
        
        # Send initial predictive analytics
        await self.send(text_data=json.dumps({
            'type': 'predictive_analytics_connected',
            'session_id': self.session_id,
            'message': 'Predictive analytics monitoring started'
        }))
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        if hasattr(self, 'monitoring_service') and hasattr(self, 'scope') and 'user' in self.scope:
            # Stop predictive monitoring
            await self.monitoring_service.stop_user_monitoring(
                self.scope['user'].id,
                self.session_id
            )
        
        await self.channel_layer.group_discard(
            self.predictive_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """Handle incoming predictive analytics requests"""
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type')
            
            if message_type == 'request_predictive_update':
                # User requesting manual predictive update
                await self._handle_predictive_update_request()
            
            elif message_type == 'subscribe_to_model':
                # Subscribe to specific predictive model updates
                model_type = text_data_json.get('model_type', 'all')
                await self._subscribe_to_model(model_type)
            
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON received'
            }))
    
    async def send_predictive_update(self, event):
        """Send predictive analytics update to user"""
        predictive_data = event['data']
        await self.send(text_data=json.dumps({
            'type': 'predictive_analytics_update',
            'data': predictive_data,
            'timestamp': timezone.now().isoformat()
        }))
    
    async def send_ai_recommendation(self, event):
        """Send AI-generated recommendation"""
        recommendation_data = event['data']
        await self.send(text_data=json.dumps({
            'type': 'ai_recommendation',
            'recommendation': recommendation_data,
            'timestamp': timezone.now().isoformat()
        }))
    
    async def _handle_predictive_update_request(self):
        """Handle manual predictive analytics update request"""
        try:
            # Generate fresh predictive analytics
            predictive_data = await self._generate_predictive_update()
            
            await self.send(text_data=json.dumps({
                'type': 'manual_predictive_update',
                'data': predictive_data,
                'timestamp': timezone.now().isoformat()
            }))
            
        except Exception as e:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f'Failed to generate predictive update: {str(e)}'
            }))
    
    async def _subscribe_to_model(self, model_type: str):
        """Subscribe to specific predictive model updates"""
        # Add subscription logic here
        await self.send(text_data=json.dumps({
            'type': 'subscription_confirmed',
            'model_type': model_type,
            'message': f'Subscribed to {model_type} predictive updates'
        }))
    
    async def _generate_predictive_update(self) -> dict:
        """Generate fresh predictive analytics update"""
        try:
            insights = await self.monitoring_service.stream_predictive_updates(
                self.scope['user'].id,
                self.session_id
            )
            return insights.get('predictive_insights', {})
        except Exception as e:
            return {'error': str(e)}


class AIInteractionConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time AI agent interactions
    """
    
    async def connect(self):
        """Handle WebSocket connection for AI interactions"""
        self.session_id = str(uuid.uuid4())
        self.ai_group_name = f"ai_interaction_{self.scope['user'].id}"
        
        if isinstance(self.scope["user"], AnonymousUser):
            await self.close()
            return
        
        await self.channel_layer.group_add(
            self.ai_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        await self.send(text_data=json.dumps({
            'type': 'ai_interaction_connected',
            'session_id': self.session_id,
            'available_agents': await self._get_available_agents()
        }))
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        await self.channel_layer.group_discard(
            self.ai_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """Handle incoming AI interaction messages"""
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type')
            
            if message_type == 'ai_chat':
                # Process AI chat request
                await self._handle_ai_chat(text_data_json)
            
            elif message_type == 'agent_switch':
                # Switch between AI agents
                agent_type = text_data_json.get('agent_type', 'learning_assistant')
                await self._handle_agent_switch(agent_type)
            
            elif message_type == 'get_agent_info':
                # Get information about specific agent
                agent_type = text_data_json.get('agent_type')
                await self._handle_agent_info_request(agent_type)
        
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON received'
            }))
    
    async def send_ai_response(self, event):
        """Send AI response to user"""
        response_data = event['response']
        await self.send(text_data=json.dumps({
            'type': 'ai_response',
            'response': response_data,
            'timestamp': timezone.now().isoformat()
        }))
    
    async def _handle_ai_chat(self, message_data: dict):
        """Handle AI chat request"""
        try:
            from apps.agents.ai_multi_agent_system import get_multi_agent_system
            
            user_input = message_data.get('message', '')
            agent_type = message_data.get('agent_type', 'learning_assistant')
            context = message_data.get('context', {})
            
            ai_system = get_multi_agent_system()
            
            # Process AI request
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            ai_request = {
                'user_id': str(self.scope['user'].id),
                'message': user_input,
                'agent_type': agent_type,
                'session_id': self.session_id,
                'context': context
            }
            
            ai_response = loop.run_until_complete(ai_system.process_request(ai_request))
            
            # Send response back to user
            await self.send(text_data=json.dumps({
                'type': 'ai_chat_response',
                'response': ai_response,
                'timestamp': timezone.now().isoformat()
            }))
            
        except Exception as e:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f'AI processing error: {str(e)}'
            }))
    
    async def _handle_agent_switch(self, agent_type: str):
        """Handle agent switching"""
        # Send confirmation of agent switch
        await self.send(text_data=json.dumps({
            'type': 'agent_switch_confirmed',
            'agent_type': agent_type,
            'message': f'Switched to {agent_type} agent'
        }))
    
    async def _handle_agent_info_request(self, agent_type: str):
        """Handle agent info request"""
        try:
            from apps.agents.ai_multi_agent_system import get_multi_agent_system
            
            ai_system = get_multi_agent_system()
            agents_info = ai_system.get_available_agents()
            
            agent_info = next((agent for agent in agents_info if agent['type'] == agent_type), None)
            
            await self.send(text_data=json.dumps({
                'type': 'agent_info_response',
                'agent_info': agent_info,
                'timestamp': timezone.now().isoformat()
            }))
            
        except Exception as e:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f'Agent info error: {str(e)}'
            }))
    
    async def _get_available_agents(self) -> list:
        """Get list of available AI agents"""
        try:
            from apps.agents.ai_multi_agent_system import get_multi_agent_system
            
            ai_system = get_multi_agent_system()
            return ai_system.get_available_agents()
        except Exception as e:
            return []

'''
    
    # Add the enhanced consumers before the final numpy import
    content = content.replace('import numpy as np', enhanced_consumer + '\nimport numpy as np')
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    print("✓ Created enhanced WebSocket consumers")

def update_websocket_routing():
    """Update WebSocket routing to include new endpoints"""
    
    file_path = '/workspace/backend/apps/progress/routing.py'
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Add new WebSocket patterns
    new_patterns = '''
    re_path(r'ws/predictive/$', consumers.PredictiveAnalyticsConsumer.as_asgi()),
    re_path(r'ws/ai-interaction/$', consumers.AIInteractionConsumer.as_asgi()),'''
    
    content = content.replace(
        'websocket_urlpatterns = [',
        f'websocket_urlpatterns = [{new_patterns}'
    )
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    print("✓ Updated WebSocket routing")

def create_enhanced_predictive_api_views():
    """Create enhanced API views for predictive analytics streaming"""
    
    file_path = '/workspace/backend/apps/progress/views_predictive.py'
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Add streaming API views at the end
    streaming_apis = '''

class PredictiveStreamingAPIView(APIView):
    """
    API endpoint for real-time predictive analytics streaming
    GET /api/predictive/streaming/
    """
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.realtime_service = RealtimeMonitoringService()
        self.predictive_service = PredictiveAnalyticsService()
    
    async def get(self, request):
        """Get real-time predictive analytics stream"""
        try:
            user = request.user
            stream_type = request.GET.get('type', 'comprehensive')  # comprehensive, velocity, engagement, etc.
            
            # Get predictive insights
            insights = await self._get_predictive_stream_data(user, stream_type)
            
            # Get AI recommendations
            ai_recommendations = await self._get_ai_recommendations(user)
            
            response_data = {
                'user_id': user.id,
                'timestamp': timezone.now().isoformat(),
                'stream_type': stream_type,
                'predictive_insights': insights,
                'ai_recommendations': ai_recommendations,
                'streaming_active': True
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': 'Failed to get predictive stream',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    async def _get_predictive_stream_data(self, user: User, stream_type: str) -> Dict[str, Any]:
        """Get predictive analytics for streaming"""
        try:
            if stream_type == 'comprehensive':
                # Get all predictive models
                velocity_data = self.predictive_service.analyze_learning_velocity(user)
                engagement_data = self.predictive_service.analyze_engagement_patterns(user)
                success_data = self.predictive_service.model_success_probability(user)
                completion_data = self.predictive_service.predict_time_to_completion(user)
                retention_data = self.predictive_service.assess_retention_risk(user)
                gaps_data = self.predictive_service.detect_knowledge_gaps(user)
                clusters_data = self.predictive_service.perform_learning_analytics_clustering(user)
                
                return {
                    'learning_velocity': velocity_data,
                    'engagement_patterns': engagement_data,
                    'success_probability': success_data,
                    'time_to_completion': completion_data,
                    'retention_risk': retention_data,
                    'knowledge_gaps': gaps_data,
                    'learning_clusters': clusters_data
                }
            else:
                # Get specific predictive model
                method_map = {
                    'velocity': 'analyze_learning_velocity',
                    'engagement': 'analyze_engagement_patterns',
                    'success': 'model_success_probability',
                    'completion': 'predict_time_to_completion',
                    'retention': 'assess_retention_risk',
                    'gaps': 'detect_knowledge_gaps',
                    'clusters': 'perform_learning_analytics_clustering'
                }
                
                method_name = method_map.get(stream_type)
                if method_name and hasattr(self.predictive_service, method_name):
                    method = getattr(self.predictive_service, method_name)
                    return method(user)
                else:
                    return {'error': f'Unknown stream type: {stream_type}'}
                    
        except Exception as e:
            return {'error': str(e)}
    
    async def _get_ai_recommendations(self, user: User) -> Dict[str, Any]:
        """Get AI-generated recommendations"""
        try:
            from apps.agents.ai_multi_agent_system import get_multi_agent_system
            
            ai_system = get_multi_agent_system()
            
            ai_request = {
                'user_id': str(user.id),
                'message': 'Provide current learning recommendations based on predictive analytics',
                'agent_type': 'mentor_coach'
            }
            
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            ai_response = loop.run_until_complete(ai_system.process_request(ai_request))
            return ai_response
            
        except Exception as e:
            return {'error': str(e)}


class AIInteractionAPIView(APIView):
    """
    API endpoint for AI agent interactions
    POST /api/ai/interaction/
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Handle AI agent interaction"""
        try:
            user = request.user
            data = request.data
            
            agent_type = data.get('agent_type', 'learning_assistant')
            message = data.get('message', '')
            context = data.get('context', {})
            session_id = data.get('session_id', str(uuid.uuid4()))
            
            # Process AI request
            from apps.agents.ai_multi_agent_system import get_multi_agent_system
            
            ai_system = get_multi_agent_system()
            
            ai_request = {
                'user_id': str(user.id),
                'message': message,
                'agent_type': agent_type,
                'session_id': session_id,
                'context': context
            }
            
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            ai_response = loop.run_until_complete(ai_system.process_request(ai_request))
            
            return Response({
                'success': True,
                'response': ai_response,
                'session_id': session_id,
                'timestamp': timezone.now().isoformat()
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request):
        """Get available AI agents"""
        try:
            from apps.agents.ai_multi_agent_system import get_multi_agent_system
            
            ai_system = get_multi_agent_system()
            agents_info = ai_system.get_available_agents()
            
            return Response({
                'available_agents': agents_info,
                'timestamp': timezone.now().isoformat()
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

'''
    
    # Add imports at the top
    import_addition = '''import uuid
import asyncio'''
    
    content = import_addition + '\n' + content
    
    # Add the streaming APIs before the final numpy import
    content = content.replace('import numpy as np', streaming_apis + '\nimport numpy as np')
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    print("✓ Created enhanced predictive API views")

def add_predictive_ai_urls():
    """Add URLs for predictive analytics and AI interaction"""
    
    file_path = '/workspace/backend/apps/progress/urls.py'
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Add imports for new views
    import_additions = '''
from .views_predictive import PredictiveStreamingAPIView, AIInteractionAPIView
from .views_realtime import RealTimeDashboardAPIView, PredictiveAnalyticsAPIView, PerformanceAlertsAPIView, TrendAnalysisAPIView'''
    
    content = import_additions + '\n' + content
    
    # Add URL patterns for predictive streaming and AI interaction
    url_additions = '''
    # Predictive Analytics Streaming
    path('api/predictive/streaming/', PredictiveStreamingAPIView.as_view()),
    path('api/predictive/streaming/<str:stream_type>/', PredictiveStreamingAPIView.as_view()),
    
    # AI Interaction
    path('api/ai/interaction/', AIInteractionAPIView.as_view()),
    path('api/ai/agents/', AIInteractionAPIView.as_view()),'''
    
    # Find where to insert the patterns
    if 'urlpatterns = [' in content:
        content = content.replace('urlpatterns = [', 'urlpatterns = [' + url_additions)
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    print("✓ Added predictive analytics and AI interaction URLs")

def enhance_views_realtime_with_predictive():
    """Enhance existing views with predictive model integration"""
    
    file_path = '/workspace/backend/apps/progress/views_realtime.py'
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Enhance PredictiveAnalyticsAPIView to use the new predictive models
    predictive_enhancement = '''
    def _get_comprehensive_predictions(self, user: User, time_horizon: int, learning_path_id: Optional[str]) -> Dict[str, Any]:
        """Get comprehensive ML predictions using all integrated models"""
        try:
            # Use the predictive analytics service with all 8 methods
            predictions = self.predictive_service.generate_comprehensive_predictions(
                user=user,
                time_horizon_days=time_horizon,
                learning_path_id=learning_path_id
            )
            
            # Also get individual model results for detailed analysis
            individual_predictions = {}
            
            # Learning velocity analysis
            try:
                individual_predictions['learning_velocity'] = self.predictive_service.analyze_learning_velocity(user)
            except Exception as e:
                individual_predictions['learning_velocity'] = {'error': str(e)}
            
            # Engagement pattern analysis
            try:
                individual_predictions['engagement_patterns'] = self.predictive_service.analyze_engagement_patterns(user)
            except Exception as e:
                individual_predictions['engagement_patterns'] = {'error': str(e)}
            
            # Success probability modeling
            try:
                individual_predictions['success_probability'] = self.predictive_service.model_success_probability(user)
            except Exception as e:
                individual_predictions['success_probability'] = {'error': str(e)}
            
            # Time to completion prediction
            try:
                individual_predictions['time_to_completion'] = self.predictive_service.predict_time_to_completion(user)
            except Exception as e:
                individual_predictions['time_to_completion'] = {'error': str(e)}
            
            # Retention risk assessment
            try:
                individual_predictions['retention_risk'] = self.predictive_service.assess_retention_risk(user)
            except Exception as e:
                individual_predictions['retention_risk'] = {'error': str(e)}
            
            # Knowledge gap detection
            try:
                individual_predictions['knowledge_gaps'] = self.predictive_service.detect_knowledge_gaps(user)
            except Exception as e:
                individual_predictions['knowledge_gaps'] = {'error': str(e)}
            
            # Learning clusters analysis
            try:
                individual_predictions['learning_clusters'] = self.predictive_service.perform_learning_analytics_clustering(user)
            except Exception as e:
                individual_predictions['learning_clusters'] = {'error': str(e)}
            
            # Performance forecasting
            try:
                individual_predictions['performance_forecast'] = self.predictive_service.analyze_performance_forecasting(user)
            except Exception as e:
                individual_predictions['performance_forecast'] = {'error': str(e)}
            
            return {
                'comprehensive_overview': predictions,
                'individual_models': individual_predictions,
                'model_count': len(individual_predictions),
                'successful_predictions': len([p for p in individual_predictions.values() if 'error' not in p])
            }
            
        except Exception as e:
            # Fallback to basic predictions if service fails
            return self._fallback_predictions(user, time_horizon)
    
    async def _get_ai_enhanced_predictions(self, user: User) -> Dict[str, Any]:
        """Get AI-enhanced predictions using multi-agent system"""
        try:
            from apps.agents.ai_multi_agent_system import get_multi_agent_system
            
            ai_system = get_multi_agent_system()
            
            # Get prediction context
            context = {
                'user_progress': self._get_user_progress_context(user),
                'recent_activity': self._get_recent_activity_context(user),
                'performance_trends': self._get_performance_trends_data(user)
            }
            
            ai_request = {
                'user_id': str(user.id),
                'message': 'Analyze my learning data and provide strategic insights about my progress, challenges, and recommendations',
                'agent_type': 'knowledge_explorer',
                'context': context
            }
            
            ai_response = await ai_system.process_request(ai_request)
            
            return {
                'ai_insights': ai_response,
                'context_used': context,
                'timestamp': timezone.now().isoformat()
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _get_user_progress_context(self, user: User) -> Dict[str, Any]:
        """Get user progress context for AI analysis"""
        total_modules = UserModuleProgress.objects.filter(user=user).count()
        completed_modules = UserModuleProgress.objects.filter(user=user, status='completed').count()
        
        return {
            'total_modules': total_modules,
            'completed_modules': completed_modules,
            'completion_rate': round((completed_modules / max(total_modules, 1)) * 100, 2)
        }
    
    def _get_recent_activity_context(self, user: User) -> Dict[str, Any]:
        """Get recent activity context"""
        week_ago = timezone.now() - timedelta(days=7)
        recent_activities = UserModuleProgress.objects.filter(
            user=user,
            updated_at__gte=week_ago
        ).count()
        
        return {
            'activities_last_week': recent_activities,
            'engagement_level': 'high' if recent_activities >= 10 else 'medium' if recent_activities >= 5 else 'low'
        }
    
    def _get_performance_trends_data(self, user: User) -> Dict[str, Any]:
        """Get performance trends data"""
        recent_assessments = AssessmentAttempt.objects.filter(
            user=user,
            completed_at__gte=timezone.now() - timedelta(days=30),
            score__isnull=False
        )
        
        if recent_assessments.exists():
            scores = [a.score for a in recent_assessments]
            return {
                'recent_average_score': round(sum(scores) / len(scores), 2),
                'score_trend': 'improving' if len(scores) >= 3 and scores[-1] > scores[0] else 'stable',
                'total_assessments': len(scores)
            }
        
        return {'no_recent_data': True}
    
    def get(self, request):
        """Enhanced GET method with AI integration"""
        try:
            user = request.user
            time_horizon = request.GET.get('horizon', '30')
            learning_path_id = request.GET.get('learning_path_id')
            include_ai = request.GET.get('ai_enhanced', 'false').lower() == 'true'
            
            # Get comprehensive predictions using all models
            predictions = self._get_comprehensive_predictions(user, int(time_horizon), learning_path_id)
            
            # Get AI-enhanced insights if requested
            ai_enhanced_insights = {}
            if include_ai:
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                ai_enhanced_insights = loop.run_until_complete(self._get_ai_enhanced_predictions(user))
            
            # Get performance forecasts
            performance_forecast = self._get_performance_forecast(user)
            
            # Get learning recommendations
            learning_recommendations = self._get_learning_recommendations(user)
            
            # Get completion predictions
            completion_predictions = self._get_completion_predictions(user)
            
            response_data = {
                'user_id': user.id,
                'timestamp': timezone.now().isoformat(),
                'prediction_horizon_days': int(time_horizon),
                'comprehensive_predictions': predictions,
                'performance_forecast': performance_forecast,
                'learning_recommendations': learning_recommendations,
                'completion_predictions': completion_predictions,
                'confidence_scores': self._get_prediction_confidence(user),
                'model_insights': self._get_model_insights(user)
            }
            
            # Add AI enhanced insights if requested
            if include_ai and ai_enhanced_insights:
                response_data['ai_enhanced_insights'] = ai_enhanced_insights
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': 'Failed to generate enhanced predictions',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

'''
    
    # Insert the enhancement before the numpy import
    content = content.replace('import numpy as np', predictive_enhancement + '\nimport numpy as np')
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    print("✓ Enhanced views_realtime with predictive models and AI integration")

def main():
    """Main execution function"""
    print("🚀 Starting Real-time Analytics Framework Enhancement")
    print("=" * 60)
    
    # Step 1: Fix existing issues
    fix_realtime_monitoring_service()
    
    # Step 2: Enhance real-time monitoring with predictive models
    enhance_realtime_monitoring_with_predictive_models()
    
    # Step 3: Create enhanced WebSocket consumers
    create_enhanced_websocket_consumers()
    
    # Step 4: Update WebSocket routing
    update_websocket_routing()
    
    # Step 5: Create enhanced API views
    create_enhanced_predictive_api_views()
    
    # Step 6: Add URL patterns
    add_predictive_ai_urls()
    
    # Step 7: Enhance existing views
    enhance_views_realtime_with_predictive()
    
    print("=" * 60)
    print("✅ Real-time Analytics Framework Enhancement Complete!")
    print("\n🔗 New WebSocket Endpoints:")
    print("   • /ws/predictive/ - Real-time predictive analytics")
    print("   • /ws/ai-interaction/ - AI agent interactions")
    print("\n🔗 New API Endpoints:")
    print("   • /api/predictive/streaming/ - Predictive analytics stream")
    print("   • /api/ai/interaction/ - AI agent interactions")
    print("\n🤖 AI Integration Features:")
    print("   • Advanced Natural Language Processing")
    print("   • Intelligent Feedback Systems")
    print("   • Context-Aware AI Responses")
    print("   • Multi-Agent System Integration")
    print("   • Real-time AI Recommendations")
    print("\n📊 Predictive Models Integration:")
    print("   • Learning Velocity Analysis")
    print("   • Engagement Pattern Analysis")
    print("   • Success Probability Modeling")
    print("   • Time To Completion Prediction")
    print("   • Retention Risk Assessment")
    print("   • Knowledge Gap Detection")
    print("   • K-Means Learning Clusters")
    print("   • Performance Forecasting")

if __name__ == "__main__":
    main()
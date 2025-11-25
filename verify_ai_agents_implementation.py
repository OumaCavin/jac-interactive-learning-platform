#!/usr/bin/env python3
"""
AI Agents System Frontend-to-Backend Integration Verification Script

This script verifies the implementation status of all requested AI agents and their 
frontend-to-backend integration components:

1. ContentCurator Agent
2. QuizMaster Agent
3. Evaluator Agent
4. ProgressTracker Agent
5. Motivator Agent
6. SystemOrchestrator Agent

Author: MiniMax Agent
Date: 2025-11-26
"""

import os
import sys
import json
import importlib.util
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add the project root to Python path
project_root = Path(__file__).parent / "backend"
sys.path.insert(0, str(project_root))

class AIAgentsVerificationSystem:
    """Comprehensive verification system for AI agents implementation"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent / "backend"
        self.agents_path = self.project_root / "apps" / "agents"
        self.verification_results = {
            'agents_files': {},
            'ai_chat_service': {},
            'api_endpoints': {},
            'multi_agent_system': {},
            'integration_status': {},
            'recommendations': []
        }
        
        # Define expected agent specifications
        self.expected_agents = {
            'content_curator': {
                'file': 'content_curator.py',
                'class_name': 'ContentCuratorAgent',
                'description': 'Content curation and learning resource management',
                'capabilities': [
                    'content_curation', 'resource_management', 'learning_path_optimization',
                    'personalized_content', 'content_recommendation'
                ]
            },
            'quiz_master': {
                'file': 'quiz_master.py',
                'class_name': 'QuizMasterAgent',
                'description': 'Quiz and assessment generation',
                'capabilities': [
                    'quiz_generation', 'assessment_creation', 'adaptive_testing',
                    'performance_analysis', 'difficulty_recommendation'
                ]
            },
            'evaluator': {
                'file': 'evaluator.py',
                'class_name': 'EvaluatorAgent',
                'description': 'Code evaluation and feedback',
                'capabilities': [
                    'code_evaluation', 'feedback_generation', 'quality_assessment',
                    'debugging_assistance', 'best_practices_guidance'
                ]
            },
            'progress_tracker': {
                'file': 'progress_tracker.py',
                'class_name': 'ProgressTrackerAgent',
                'description': 'Learning progress tracking and analytics',
                'capabilities': [
                    'progress_tracking', 'learning_analytics', 'performance_visualization',
                    'achievement_tracking', 'learning_optimization'
                ]
            },
            'motivator': {
                'file': 'motivator.py',
                'class_name': 'MotivatorAgent',
                'description': 'User motivation and engagement',
                'capabilities': [
                    'user_encouragement', 'motivation_messages', 'engagement_tracking',
                    'goal_setting_support', 'gamification_elements'
                ]
            },
            'system_orchestrator': {
                'file': 'system_orchestrator.py',
                'class_name': 'SystemOrchestratorAgent',
                'description': 'Agent coordination and system orchestration',
                'capabilities': [
                    'agent_coordination', 'workflow_orchestration', 'system_monitoring',
                    'performance_optimization', 'resource_allocation'
                ]
            }
        }
    
    def verify_agent_files(self) -> Dict[str, Any]:
        """Verify existence and basic structure of agent files"""
        print("\n🔍 Verifying Agent Files...")
        
        file_status = {}
        
        for agent_key, agent_spec in self.expected_agents.items():
            file_path = self.agents_path / agent_spec['file']
            
            status = {
                'exists': file_path.exists(),
                'file_path': str(file_path),
                'file_size': 0,
                'has_class': False,
                'class_name': None,
                'method_count': 0,
                'line_count': 0
            }
            
            if status['exists']:
                try:
                    # Read file content
                    content = file_path.read_text(encoding='utf-8')
                    status['file_size'] = file_path.stat().st_size
                    status['line_count'] = len(content.splitlines())
                    
                    # Check for class definition
                    class_pattern = f"class {agent_spec['class_name']}"
                    status['has_class'] = class_pattern in content
                    
                    if status['has_class']:
                        status['class_name'] = agent_spec['class_name']
                        
                        # Count methods
                        method_lines = [line for line in content.splitlines() 
                                      if line.strip().startswith('def ') or line.strip().startswith('async def ')]
                        status['method_count'] = len(method_lines)
                    
                    # Check for capabilities
                    capabilities_found = []
                    for capability in agent_spec['capabilities']:
                        if capability.lower() in content.lower():
                            capabilities_found.append(capability)
                    
                    status['capabilities_found'] = capabilities_found
                    status['capability_coverage'] = len(capabilities_found) / len(agent_spec['capabilities'])
                    
                except Exception as e:
                    status['error'] = str(e)
            
            file_status[agent_key] = status
            print(f"  ✓ {agent_key}: {'✅ Found' if status['exists'] else '❌ Missing'}")
            if status['exists']:
                print(f"    - Class: {status['class_name'] or 'Not found'}")
                print(f"    - Methods: {status['method_count']}")
                print(f"    - Lines: {status['line_count']}")
                print(f"    - Capabilities: {status['capability_coverage']:.1%}")
        
        self.verification_results['agents_files'] = file_status
        return file_status
    
    def verify_ai_chat_service(self) -> Dict[str, Any]:
        """Verify AI chat service integration"""
        print("\n🔍 Verifying AI Chat Service Integration...")
        
        chat_service_path = self.agents_path / "ai_chat_service.py"
        
        if not chat_service_path.exists():
            return {'error': 'AI Chat Service file not found'}
        
        try:
            content = chat_service_path.read_text(encoding='utf-8')
            
            # Check for supported agent types
            supported_agents = []
            agent_patterns = [
                ('content_curator', 'content_curator'),
                ('quiz_master', 'quiz_master'),
                ('evaluator', 'evaluator'),
                ('progress_tracker', 'progress_tracker'),
                ('motivator', 'motivator'),
                ('system_orchestrator', 'system_orchestrator')
            ]
            
            for agent_key, pattern in agent_patterns:
                if pattern in content:
                    supported_agents.append(agent_key)
            
            # Check for key methods
            key_methods = [
                '_generate_content_response',
                '_generate_quiz_response',
                '_generate_evaluation_response',
                '_generate_progress_response',
                '_generate_motivation_response',
                '_generate_general_response'
            ]
            
            methods_found = [method for method in key_methods if method in content]
            
            # Check for JAC content provider
            has_jac_provider = 'JACAIContentProvider' in content
            
            chat_service_status = {
                'exists': True,
                'supported_agents': supported_agents,
                'supported_count': len(supported_agents),
                'total_expected': len(self.expected_agents),
                'coverage_percentage': (len(supported_agents) / len(self.expected_agents)) * 100,
                'key_methods': methods_found,
                'methods_count': len(methods_found),
                'has_jac_provider': has_jac_provider,
                'file_size': chat_service_path.stat().st_size,
                'line_count': len(content.splitlines())
            }
            
            print(f"  ✓ AI Chat Service: ✅ Found")
            print(f"    - Supported Agents: {len(supported_agents)}/6")
            print(f"    - Coverage: {chat_service_status['coverage_percentage']:.1f}%")
            print(f"    - Key Methods: {len(methods_found)}/6")
            print(f"    - JAC Provider: {'✅' if has_jac_provider else '❌'}")
            
        except Exception as e:
            chat_service_status = {'error': str(e)}
        
        self.verification_results['ai_chat_service'] = chat_service_status
        return chat_service_status
    
    def verify_api_endpoints(self) -> Dict[str, Any]:
        """Verify API endpoints and URL configurations"""
        print("\n🔍 Verifying API Endpoints...")
        
        endpoints_status = {}
        
        # Check agents URLs
        agents_urls = self.agents_path / "urls.py"
        if agents_urls.exists():
            content = agents_urls.read_text(encoding='utf-8')
            
            # Check for chat assistant endpoints
            chat_endpoints = [
                'chat-assistant/message',
                'chat-assistant/history',
                'chat-assistant/rate',
                'chat-assistant/sessions'
            ]
            
            found_endpoints = [ep for ep in chat_endpoints if ep in content]
            
            endpoints_status['agents_urls'] = {
                'exists': True,
                'chat_endpoints': found_endpoints,
                'chat_endpoint_count': len(found_endpoints),
                'has_agent_status': 'agents/status' in content
            }
            
            print(f"  ✓ Agents URLs: ✅ Found")
            print(f"    - Chat Endpoints: {len(found_endpoints)}/4")
        
        # Check AI agents URLs
        ai_agents_urls_path = self.project_root / "apps" / "api_endpoints" / "ai_agents_urls.py"
        if ai_agents_urls_path.exists():
            content = ai_agents_urls_path.read_text(encoding='utf-8')
            
            endpoints_status['ai_agents_urls'] = {
                'exists': True,
                'has_router': 'DefaultRouter' in content,
                'has_ai_agents_endpoint': 'ai-agents' in content
            }
            
            print(f"  ✓ AI Agents URLs: ✅ Found")
        
        # Check views for agent handling
        views_path = self.agents_path / "views.py"
        if views_path.exists():
            content = views_path.read_text(encoding='utf-8')
            
            # Check for chat assistant views
            has_chat_assistant = 'ChatAssistantAPIView' in content
            has_agent_views = 'AgentViewSet' in content
            
            endpoints_status['views'] = {
                'exists': True,
                'has_chat_assistant': has_chat_assistant,
                'has_agent_views': has_agent_views,
                'agent_types_handled': []
            }
            
            # Check for specific agent type handling
            agent_types = ['content_curator', 'quiz_master', 'evaluator', 
                          'progress_tracker', 'motivator', 'system_orchestrator']
            
            handled_types = [at for at in agent_types if at in content]
            endpoints_status['views']['agent_types_handled'] = handled_types
            
            print(f"  ✓ Agent Views: ✅ Found")
            print(f"    - Chat Assistant: {'✅' if has_chat_assistant else '❌'}")
            print(f"    - Agent Types Handled: {len(handled_types)}/6")
        
        self.verification_results['api_endpoints'] = endpoints_status
        return endpoints_status
    
    def verify_multi_agent_system(self) -> Dict[str, Any]:
        """Verify multi-agent system integration"""
        print("\n🔍 Verifying Multi-Agent System Integration...")
        
        multi_agent_path = self.agents_path / "ai_multi_agent_system.py"
        
        if not multi_agent_path.exists():
            return {'error': 'Multi-Agent System file not found'}
        
        try:
            content = multi_agent_path.read_text(encoding='utf-8')
            
            # Check for Gemini AI integration
            has_gemini = 'google.generativeai' in content
            has_gemini_config = 'GeminiAIConfig' in content
            
            # Check for agent classes
            expected_agent_classes = [
                'AIAgent',
                'MultiAgentSystem',
                'GeminiAIConfig'
            ]
            
            classes_found = [cls for cls in expected_agent_classes if cls in content]
            
            # Check for specialized agent personalities
            personalities = [
                'learning_assistant',
                'code_reviewer', 
                'content_generator',
                'knowledge_explorer',
                'mentor_coach'
            ]
            
            personalities_found = [p for p in personalities if p in content]
            
            multi_agent_status = {
                'exists': True,
                'has_gemini_integration': has_gemini,
                'has_gemini_config': has_gemini_config,
                'classes_found': classes_found,
                'class_count': len(classes_found),
                'personalities_found': personalities_found,
                'personality_count': len(personalities_found),
                'file_size': multi_agent_path.stat().st_size,
                'line_count': len(content.splitlines())
            }
            
            print(f"  ✓ Multi-Agent System: ✅ Found")
            print(f"    - Gemini Integration: {'✅' if has_gemini else '❌'}")
            print(f"    - Agent Personalities: {len(personalities_found)}/5")
            print(f"    - Classes: {len(classes_found)}/3")
            
        except Exception as e:
            multi_agent_status = {'error': str(e)}
        
        self.verification_results['multi_agent_system'] = multi_agent_status
        return multi_agent_status
    
    def analyze_integration_status(self) -> Dict[str, Any]:
        """Analyze overall integration status"""
        print("\n🔍 Analyzing Integration Status...")
        
        # Calculate completion scores
        agent_files_score = 0
        if self.verification_results['agents_files']:
            total_agents = len(self.expected_agents)
            found_agents = sum(1 for status in self.verification_results['agents_files'].values() 
                             if status.get('exists', False))
            agent_files_score = (found_agents / total_agents) * 100
        
        chat_service_score = 0
        if self.verification_results['ai_chat_service']:
            chat_service_score = self.verification_results['ai_chat_service'].get('coverage_percentage', 0)
        
        endpoints_score = 0
        if self.verification_results['api_endpoints']:
            endpoints_parts = []
            if 'agents_urls' in self.verification_results['api_endpoints']:
                chat_ep_score = (self.verification_results['api_endpoints']['agents_urls'].get('chat_endpoint_count', 0) / 4) * 100
                endpoints_parts.append(chat_ep_score)
            if 'views' in self.verification_results['api_endpoints']:
                agent_types_score = (len(self.verification_results['api_endpoints']['views'].get('agent_types_handled', [])) / 6) * 100
                endpoints_parts.append(agent_types_score)
            endpoints_score = sum(endpoints_parts) / len(endpoints_parts) if endpoints_parts else 0
        
        multi_agent_score = 0
        if self.verification_results['multi_agent_system']:
            if self.verification_results['multi_agent_system'].get('has_gemini_integration'):
                multi_agent_score = 80
            if self.verification_results['multi_agent_system'].get('personality_count', 0) > 0:
                multi_agent_score += 20
        
        overall_score = (agent_files_score + chat_service_score + endpoints_score + multi_agent_score) / 4
        
        integration_status = {
            'agent_files_score': agent_files_score,
            'chat_service_score': chat_service_score,
            'endpoints_score': endpoints_score,
            'multi_agent_score': multi_agent_score,
            'overall_score': overall_score,
            'status_level': self._get_status_level(overall_score),
            'completion_percentage': overall_score
        }
        
        print(f"  📊 Integration Scores:")
        print(f"    - Agent Files: {agent_files_score:.1f}%")
        print(f"    - Chat Service: {chat_service_score:.1f}%")
        print(f"    - API Endpoints: {endpoints_score:.1f}%")
        print(f"    - Multi-Agent System: {multi_agent_score:.1f}%")
        print(f"    - Overall: {overall_score:.1f}% ({integration_status['status_level']})")
        
        self.verification_results['integration_status'] = integration_status
        return integration_status
    
    def generate_recommendations(self) -> List[str]:
        """Generate recommendations for improving implementation"""
        recommendations = []
        
        # Check for missing agent files
        missing_agents = []
        for agent_key, status in self.verification_results['agents_files'].items():
            if not status.get('exists', False):
                missing_agents.append(agent_key)
        
        if missing_agents:
            recommendations.append(f"Create missing agent files: {', '.join(missing_agents)}")
        
        # Check for incomplete agent coverage
        incomplete_agents = []
        for agent_key, status in self.verification_results['agents_files'].items():
            if status.get('exists', False) and status.get('capability_coverage', 0) < 0.8:
                incomplete_agents.append(agent_key)
        
        if incomplete_agents:
            recommendations.append(f"Enhance capability coverage for: {', '.join(incomplete_agents)}")
        
        # Check chat service coverage
        if self.verification_results['ai_chat_service'].get('coverage_percentage', 0) < 100:
            missing_agent_types = set(self.expected_agents.keys()) - set(self.verification_results['ai_chat_service'].get('supported_agents', []))
            recommendations.append(f"Add chat service support for: {', '.join(missing_agent_types)}")
        
        # Check API endpoints
        if self.verification_results['api_endpoints'].get('agents_urls', {}).get('chat_endpoint_count', 0) < 4:
            recommendations.append("Complete chat assistant API endpoints implementation")
        
        # Check for Gemini integration
        if not self.verification_results['multi_agent_system'].get('has_gemini_integration', False):
            recommendations.append("Implement Google Gemini AI integration in multi-agent system")
        
        # General recommendations
        if self.verification_results['integration_status'].get('overall_score', 0) < 90:
            recommendations.append("Complete frontend integration testing and WebSocket connectivity")
            recommendations.append("Implement comprehensive error handling and logging")
            recommendations.append("Add integration tests for agent interactions")
        
        self.verification_results['recommendations'] = recommendations
        return recommendations
    
    def _get_status_level(self, score: float) -> str:
        """Get status level description based on score"""
        if score >= 90:
            return "EXCELLENT"
        elif score >= 80:
            return "GOOD"
        elif score >= 70:
            return "FAIR"
        elif score >= 50:
            return "PARTIAL"
        else:
            return "INCOMPLETE"
    
    def generate_comprehensive_report(self) -> str:
        """Generate comprehensive verification report"""
        report = []
        
        report.append("# AI Agents System - Frontend-to-Backend Integration Verification Report")
        report.append(f"**Generated on:** {self._get_timestamp()}")
        report.append(f"**Overall Completion:** {self.verification_results['integration_status'].get('overall_score', 0):.1f}%")
        report.append("")
        
        # Executive Summary
        report.append("## Executive Summary")
        overall_score = self.verification_results['integration_status'].get('overall_score', 0)
        status_level = self.verification_results['integration_status'].get('status_level', 'UNKNOWN')
        
        if overall_score >= 80:
            report.append("✅ **IMPLEMENTATION STATUS: EXCELLENT**")
            report.append("The AI agents system is well-implemented with comprehensive frontend-to-backend integration.")
        elif overall_score >= 60:
            report.append("⚠️ **IMPLEMENTATION STATUS: GOOD WITH GAPS**")
            report.append("The AI agents system is largely implemented but has some gaps that need addressing.")
        else:
            report.append("❌ **IMPLEMENTATION STATUS: INCOMPLETE**")
            report.append("The AI agents system requires significant additional implementation.")
        
        report.append("")
        
        # Detailed Results
        report.append("## Detailed Verification Results")
        
        # Agent Files
        report.append("### 1. Agent Files Implementation")
        for agent_key, status in self.verification_results['agents_files'].items():
            agent_name = agent_key.replace('_', ' ').title()
            if status.get('exists'):
                report.append(f"✅ **{agent_name}**: Implemented")
                report.append(f"   - File: `{status['file_path']}`")
                report.append(f"   - Class: {status.get('class_name', 'N/A')}")
                report.append(f"   - Methods: {status.get('method_count', 0)}")
                report.append(f"   - Capabilities: {status.get('capability_coverage', 0):.1%}")
            else:
                report.append(f"❌ **{agent_name}**: Missing")
        
        report.append("")
        
        # Chat Service
        report.append("### 2. AI Chat Service Integration")
        chat_status = self.verification_results['ai_chat_service']
        if 'error' not in chat_status:
            report.append(f"✅ **Chat Service**: {chat_status.get('coverage_percentage', 0):.1f}% Complete")
            report.append(f"- Supported Agents: {chat_status.get('supported_count', 0)}/6")
            report.append(f"- Key Methods: {chat_status.get('methods_count', 0)}/6")
            report.append(f"- JAC Content Provider: {'✅' if chat_status.get('has_jac_provider') else '❌'}")
        else:
            report.append(f"❌ **Chat Service**: {chat_status['error']}")
        
        report.append("")
        
        # API Endpoints
        report.append("### 3. API Endpoints")
        endpoints = self.verification_results['api_endpoints']
        
        if 'agents_urls' in endpoints:
            report.append("✅ **Agent URLs**: Configured")
            report.append(f"- Chat Endpoints: {endpoints['agents_urls'].get('chat_endpoint_count', 0)}/4")
        
        if 'views' in endpoints:
            report.append("✅ **Agent Views**: Implemented")
            report.append(f"- Chat Assistant: {'✅' if endpoints['views'].get('has_chat_assistant') else '❌'}")
            report.append(f"- Agent Types: {len(endpoints['views'].get('agent_types_handled', []))}/6")
        
        report.append("")
        
        # Multi-Agent System
        report.append("### 4. Multi-Agent System")
        ma_status = self.verification_results['multi_agent_system']
        if 'error' not in ma_status:
            report.append(f"✅ **Multi-Agent System**: Implemented")
            report.append(f"- Gemini Integration: {'✅' if ma_status.get('has_gemini_integration') else '❌'}")
            report.append(f"- Agent Personalities: {ma_status.get('personality_count', 0)}/5")
            report.append(f"- Classes: {ma_status.get('class_count', 0)}/3")
        else:
            report.append(f"❌ **Multi-Agent System**: {ma_status['error']}")
        
        report.append("")
        
        # Frontend Integration Status
        report.append("## Frontend Integration Status")
        report.append("### WebSocket Endpoints")
        report.append("The following WebSocket endpoints should be available for real-time agent communication:")
        ws_endpoints = [
            "/ws/dashboard/ - General dashboard updates",
            "/ws/predictive/ - Predictive analytics",
            "/ws/ai-interaction/ - AI agent conversations",
            "/ws/alerts/ - System notifications",
            "/ws/metrics/ - Real-time metrics",
            "/ws/activity/ - User activity updates"
        ]
        for endpoint in ws_endpoints:
            report.append(f"- {endpoint}")
        
        report.append("")
        report.append("### REST API Endpoints")
        report.append("The following REST API endpoints are available for agent interactions:")
        api_endpoints = [
            "POST /api/agents/chat-assistant/message/ - Send message to agent",
            "GET /api/agents/chat-assistant/history/ - Get conversation history", 
            "POST /api/agents/chat-assistant/rate/{message_id}/ - Rate agent response",
            "GET /api/agents/chat-assistant/sessions/ - List chat sessions",
            "GET /api/agents/agents/status/ - Get agent system status"
        ]
        for endpoint in api_endpoints:
            report.append(f"- {endpoint}")
        
        report.append("")
        
        # Agent Capabilities
        report.append("## Agent Capabilities Overview")
        for agent_key, agent_spec in self.expected_agents.items():
            agent_name = agent_key.replace('_', ' ').title()
            report.append(f"### {agent_name}")
            report.append(f"**File:** `{agent_spec['file']}`")
            report.append(f"**Description:** {agent_spec['description']}")
            report.append("**Key Capabilities:**")
            for capability in agent_spec['capabilities']:
                report.append(f"- {capability.replace('_', ' ').title()}")
            report.append("")
        
        # Recommendations
        report.append("## Recommendations")
        if self.verification_results['recommendations']:
            for i, rec in enumerate(self.verification_results['recommendations'], 1):
                report.append(f"{i}. {rec}")
        else:
            report.append("✅ No critical recommendations - implementation is comprehensive!")
        
        report.append("")
        
        # Next Steps
        report.append("## Next Steps for Complete Implementation")
        if overall_score < 90:
            report.append("1. **Address Missing Components**: Focus on any items marked as missing or incomplete")
            report.append("2. **Frontend Integration**: Ensure React components properly connect to WebSocket and REST endpoints")
            report.append("3. **Testing**: Implement comprehensive integration tests for agent interactions")
            report.append("4. **Error Handling**: Add robust error handling and logging throughout the system")
            report.append("5. **Performance Optimization**: Monitor and optimize agent response times")
        else:
            report.append("1. **Production Deployment**: System is ready for production deployment")
            report.append("2. **Monitoring**: Set up comprehensive monitoring for agent performance")
            report.append("3. **User Feedback**: Collect and analyze user feedback on agent interactions")
            report.append("4. **Continuous Improvement**: Regularly update and enhance agent capabilities")
        
        return "\n".join(report)
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    def run_comprehensive_verification(self) -> Dict[str, Any]:
        """Run complete verification process"""
        print("🚀 Starting AI Agents System Frontend-to-Backend Integration Verification")
        print("=" * 80)
        
        # Run all verification steps
        self.verify_agent_files()
        self.verify_ai_chat_service()
        self.verify_api_endpoints()
        self.verify_multi_agent_system()
        self.analyze_integration_status()
        self.generate_recommendations()
        
        return self.verification_results


def main():
    """Main verification function"""
    verification_system = AIAgentsVerificationSystem()
    
    try:
        # Run comprehensive verification
        results = verification_system.run_comprehensive_verification()
        
        # Generate and save report
        report = verification_system.generate_comprehensive_report()
        
        # Save report to file
        report_path = Path(__file__).parent / "AI_AGENTS_IMPLEMENTATION_REPORT.md"
        report_path.write_text(report, encoding='utf-8')
        
        print("\n" + "=" * 80)
        print("📋 VERIFICATION COMPLETE")
        print("=" * 80)
        
        overall_score = results['integration_status'].get('overall_score', 0)
        status_level = results['integration_status'].get('status_level', 'UNKNOWN')
        
        print(f"🎯 Overall Completion: {overall_score:.1f}% ({status_level})")
        print(f"📄 Detailed Report: {report_path}")
        
        # Show quick summary
        print("\n🔍 Quick Summary:")
        agent_count = len([s for s in results['agents_files'].values() if s.get('exists', False)])
        print(f"  - Agent Files: {agent_count}/6 implemented")
        
        if 'ai_chat_service' in results and 'coverage_percentage' in results['ai_chat_service']:
            print(f"  - Chat Service: {results['ai_chat_service']['coverage_percentage']:.1f}% coverage")
        
        if 'api_endpoints' in results:
            chat_eps = results['api_endpoints'].get('agents_urls', {}).get('chat_endpoint_count', 0)
            print(f"  - API Endpoints: {chat_eps}/4 chat endpoints")
        
        print("\n✅ Verification completed successfully!")
        
        return results
        
    except Exception as e:
        print(f"\n❌ Verification failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    main()
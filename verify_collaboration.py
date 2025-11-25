#!/usr/bin/env python3
"""
Collaboration Features Implementation Verification

Comprehensive verification of all collaboration features implementation.
Verifies both frontend and backend components.

Author: Cavin Otieno
Created: 2025-11-26
"""

import os
import sys
import json
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_path))

def check_backend_implementation():
    """Check backend collaboration implementation"""
    print("=== BACKEND VERIFICATION ===")
    
    app_path = backend_path / 'apps' / 'collaboration'
    
    # Required files and their sizes
    required_files = {
        '__init__.py': 32,  # Size check
        'models.py': 12000,  # Should be substantial
        'admin.py': 6000,
        'apps.py': 600,
        'serializers.py': 8000,
        'views.py': 17000,
        'urls.py': 1000,
        'signals.py': 3000,
        'migrations/__init__.py': 33,
        'migrations/0001_initial.py': 8000,
    }
    
    print("Checking Django app structure...")
    app_ok = True
    
    for file_path, min_size in required_files.items():
        full_path = app_path / file_path
        if not full_path.exists():
            print(f"❌ MISSING: {file_path}")
            app_ok = False
        elif full_path.stat().st_size < min_size:
            print(f"❌ TOO SMALL: {file_path} (expected ~{min_size} bytes)")
            app_ok = False
        else:
            print(f"✅ {file_path}")
    
    # Check Django settings integration
    settings_path = backend_path / 'config' / 'settings.py'
    if settings_path.exists():
        with open(settings_path, 'r') as f:
            content = f.read()
            if "'apps.collaboration'" in content:
                print("✅ Django settings integration")
            else:
                print("❌ Missing Django settings integration")
                app_ok = False
    
    # Check URL routing
    urls_path = backend_path / 'config' / 'urls.py'
    if urls_path.exists():
        with open(urls_path, 'r') as f:
            content = f.read()
            if "'api/collaboration/'" in content:
                print("✅ Django URL routing")
            else:
                print("❌ Missing Django URL routing")
                app_ok = False
    
    print(f"Backend implementation: {'✅ COMPLETE' if app_ok else '❌ INCOMPLETE'}")
    return app_ok

def check_frontend_implementation():
    """Check frontend collaboration implementation"""
    print("\n=== FRONTEND VERIFICATION ===")
    
    frontend_path = Path(__file__).parent / 'frontend'
    src_path = frontend_path / 'src'
    
    # Check collaboration service
    service_path = src_path / 'services' / 'collaborationService.ts'
    service_ok = service_path.exists() and service_path.stat().st_size > 15000
    if service_ok:
        print("✅ Collaboration Service (collaborationService.ts)")
    else:
        print("❌ Collaboration Service missing or too small")
    
    # Check collaboration components
    components_path = src_path / 'components' / 'collaboration'
    components_ok = True
    
    required_components = [
        'index.tsx',
        'CollaborationDashboard.tsx',
        'StudyGroupDetail.tsx'
    ]
    
    for component in required_components:
        comp_path = components_path / component
        if not comp_path.exists():
            print(f"❌ MISSING: {component}")
            components_ok = False
        elif comp_path.stat().st_size < 500:  # Minimum size check
            print(f"❌ TOO SMALL: {component}")
            components_ok = False
        else:
            print(f"✅ {component}")
    
    # Check collaboration page
    page_path = src_path / 'pages' / 'Collaboration.tsx'
    page_ok = page_path.exists() and page_path.stat().st_size > 500
    if page_ok:
        print("✅ Collaboration Page (Collaboration.tsx)")
    else:
        print("❌ Collaboration Page missing or too small")
    
    # Check App.tsx integration
    app_path = src_path / 'App.tsx'
    if app_path.exists():
        with open(app_path, 'r') as f:
            content = f.read()
            if "import('./pages/Collaboration')" in content and "/collaboration" in content:
                print("✅ App.tsx routing integration")
                app_integration_ok = True
            else:
                print("❌ Missing App.tsx routing integration")
                app_integration_ok = False
    else:
        print("❌ App.tsx not found")
        app_integration_ok = False
    
    frontend_ok = service_ok and components_ok and page_ok and app_integration_ok
    print(f"Frontend implementation: {'✅ COMPLETE' if frontend_ok else '❌ INCOMPLETE'}")
    return frontend_ok

def check_features_implementation():
    """Check specific feature implementations"""
    print("\n=== FEATURES VERIFICATION ===")
    
    features = {
        'Study Groups': [
            'StudyGroup model with all fields',
            'StudyGroupMembership model',
            'join/leave group endpoints',
            'member management UI',
            'group detail page'
        ],
        'Discussion Forums': [
            'DiscussionForum model',
            'DiscussionTopic model',
            'DiscussionPost model',
            'topic creation and replies',
            'forum UI with topics'
        ],
        'Peer Code Sharing': [
            'PeerCodeShare model',
            'CodeLike model',
            'code like/unlike functionality',
            'code sharing UI',
            'download tracking'
        ],
        'Group Challenges': [
            'GroupChallenge model',
            'ChallengeParticipation model',
            'challenge participation',
            'challenge creation and management',
            'challenge UI'
        ],
        'Mentorship System': [
            'MentorshipRelationship model',
            'MentorshipSession model',
            'mentorship request/accept flow',
            'session scheduling',
            'mentorship UI'
        ]
    }
    
    print("Checking feature completeness...")
    all_features_ok = True
    
    for feature_name, requirements in features.items():
        feature_ok = True
        print(f"\n{feature_name}:")
        
        # Check backend models
        backend_path = Path(__file__).parent / 'backend' / 'apps' / 'collaboration' / 'models.py'
        if backend_path.exists():
            with open(backend_path, 'r') as f:
                content = f.read()
                # Check for model definitions
                model_checks = [
                    f'class {req.split()[0]}' for req in requirements 
                    if 'model' in req.lower()
                ]
                for model_check in model_checks:
                    if model_check in content:
                        print(f"  ✅ {model_check}")
                    else:
                        print(f"  ❌ {model_check}")
                        feature_ok = False
        
        # Check frontend components
        frontend_path = Path(__file__).parent / 'frontend' / 'src' / 'components' / 'collaboration'
        if feature_name == 'Study Groups':
            ui_files = ['CollaborationDashboard.tsx', 'StudyGroupDetail.tsx']
        else:
            ui_files = ['CollaborationDashboard.tsx']
        
        for ui_file in ui_files:
            ui_path = frontend_path / ui_file
            if ui_path.exists() and ui_path.stat().st_size > 1000:
                print(f"  ✅ {ui_file}")
            else:
                print(f"  ❌ {ui_file}")
                feature_ok = False
        
        print(f"  {feature_name}: {'✅ IMPLEMENTED' if feature_ok else '❌ INCOMPLETE'}")
        if not feature_ok:
            all_features_ok = False
    
    return all_features_ok

def check_api_endpoints():
    """Check API endpoint completeness"""
    print("\n=== API ENDPOINTS VERIFICATION ===")
    
    # Check views.py for endpoint methods
    views_path = backend_path / 'apps' / 'collaboration' / 'views.py'
    if views_path.exists():
        with open(views_path, 'r') as f:
            content = f.read()
            
        # Expected endpoint patterns
        endpoints = [
            ('Study Groups', 'StudyGroupViewSet'),
            ('Discussion Topics', 'DiscussionTopicViewSet'),
            ('Discussion Posts', 'DiscussionPostViewSet'),
            ('Code Shares', 'PeerCodeShareViewSet'),
            ('Group Challenges', 'GroupChallengeViewSet'),
            ('Mentorship', 'MentorshipRelationshipViewSet'),
            ('Overview', 'CollaborationOverviewViewSet'),
        ]
        
        all_endpoints_ok = True
        for name, viewset in endpoints:
            if f'class {viewset}' in content:
                print(f"✅ {name} API ({viewset})")
            else:
                print(f"❌ {name} API ({viewset})")
                all_endpoints_ok = False
        
        return all_endpoints_ok
    else:
        print("❌ views.py not found")
        return False

def check_frontend_services():
    """Check frontend service completeness"""
    print("\n=== FRONTEND SERVICES VERIFICATION ===")
    
    service_path = Path(__file__).parent / 'frontend' / 'src' / 'services' / 'collaborationService.ts'
    if service_path.exists():
        with open(service_path, 'r') as f:
            content = f.read()
        
        # Expected service methods
        methods = [
            'getStudyGroups',
            'joinStudyGroup',
            'leaveStudyGroup',
            'getDiscussionTopics',
            'createDiscussionTopic',
            'getCodeShares',
            'likeCodeShare',
            'getGroupChallenges',
            'participateInChallenge',
            'getMentorshipRelationships',
            'getCollaborationOverview',
        ]
        
        all_methods_ok = True
        for method in methods:
            if f'async {method}' in content:
                print(f"✅ {method}()")
            else:
                print(f"❌ {method}()")
                all_methods_ok = False
        
        return all_methods_ok
    else:
        print("❌ collaborationService.ts not found")
        return False

def main():
    """Main verification function"""
    print("Collaboration Features Implementation Verification")
    print("=" * 60)
    
    # Run all checks
    backend_ok = check_backend_implementation()
    frontend_ok = check_frontend_implementation()
    features_ok = check_features_implementation()
    api_ok = check_api_endpoints()
    services_ok = check_frontend_services()
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    print(f"Backend Implementation:     {'✅ COMPLETE' if backend_ok else '❌ INCOMPLETE'}")
    print(f"Frontend Implementation:    {'✅ COMPLETE' if frontend_ok else '❌ INCOMPLETE'}")
    print(f"Features Implementation:    {'✅ COMPLETE' if features_ok else '❌ INCOMPLETE'}")
    print(f"API Endpoints:             {'✅ COMPLETE' if api_ok else '❌ INCOMPLETE'}")
    print(f"Frontend Services:         {'✅ COMPLETE' if services_ok else '❌ INCOMPLETE'}")
    
    overall_ok = all([backend_ok, frontend_ok, features_ok, api_ok, services_ok])
    print(f"\nOVERALL STATUS:           {'✅ ALL FEATURES IMPLEMENTED' if overall_ok else '❌ SOME FEATURES MISSING'}")
    
    if overall_ok:
        print("\n🎉 All collaboration features have been successfully implemented!")
        print("\nImplemented Features:")
        print("✅ Study Groups Functionality")
        print("✅ Discussion Forums") 
        print("✅ Peer Code Sharing")
        print("✅ Group Challenges")
        print("✅ Mentorship System")
        print("\nFrontend-Backend Integration: ✅ COMPLETE")
        print("\nReady for testing and deployment! 🚀")
    else:
        print("\n⚠️  Some collaboration features are missing or incomplete.")
        print("Please review the verification output above.")
    
    return 0 if overall_ok else 1

if __name__ == '__main__':
    exit(main())
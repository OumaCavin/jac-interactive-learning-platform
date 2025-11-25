#!/usr/bin/env python3
"""
Adaptive Learning System Integration Test

This script tests the complete frontend-to-backend integration of the adaptive learning system.
It demonstrates the challenge generation, difficulty adjustment, and performance tracking features.

Note: This test script assumes the backend APIs are running and accessible.
"""

import requests
import json
import time
from datetime import datetime, timedelta
import sys

class AdaptiveLearningTester:
    def __init__(self, base_url="http://localhost:8000", token=None):
        self.base_url = base_url
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}' if token else ''
        }
        self.test_results = []

    def log_test(self, test_name, success, message, details=None):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        
        if details and not success:
            print(f"    Details: {details}")
            
        self.test_results.append({
            'test': test_name,
            'success': success,
            'message': message,
            'details': details
        })

    def test_api_endpoint(self, method, endpoint, data=None, expected_status=None):
        """Test API endpoint"""
        try:
            url = f"{self.base_url}{endpoint}"
            
            if method.upper() == 'GET':
                response = requests.get(url, headers=self.headers)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=self.headers, json=data)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            if expected_status and response.status_code != expected_status:
                return False, f"Expected status {expected_status}, got {response.status_code}", response.text
            
            return True, "Success", response.json() if response.content else {}
            
        except requests.exceptions.RequestException as e:
            return False, f"Request failed: {str(e)}", None
        except json.JSONDecodeError as e:
            return False, f"JSON decode error: {str(e)}", response.text if response else None

    def test_user_authentication(self):
        """Test user authentication flow"""
        print("\n🔐 Testing User Authentication")
        
        # Test login (assuming we have test credentials)
        success, message, data = self.test_api_endpoint(
            'POST', 
            '/api/auth/login/', 
            {
                'username': 'testuser',
                'password': 'testpassword'
            }
        )
        
        if success and 'access' in data:
            self.token = data['access']
            self.headers['Authorization'] = f'Bearer {self.token}'
            self.log_test("User Login", True, "Successfully authenticated and received token")
            return True
        else:
            self.log_test("User Login", False, "Failed to authenticate", message)
            # Continue without authentication for public endpoints
            return False

    def test_challenge_generation(self):
        """Test adaptive challenge generation"""
        print("\n🧠 Testing Challenge Generation")
        
        # Test challenge generation
        success, message, data = self.test_api_endpoint(
            'POST',
            '/api/adaptive-challenges/generate/',
            {
                'challenge_type': 'quiz',
                'specific_topic': 'JAC object creation'
            }
        )
        
        if success and data.get('success'):
            challenge = data.get('challenge')
            personalization = data.get('personalization')
            
            # Validate challenge structure
            required_fields = ['id', 'title', 'description', 'challenge_type', 'content', 'difficulty_level']
            missing_fields = [field for field in required_fields if field not in challenge]
            
            if not missing_fields:
                self.log_test("Challenge Generation", True, f"Generated {challenge['challenge_type']} challenge successfully")
                
                # Test personalization data
                if personalization and all(k in personalization for k in ['difficulty_level', 'skill_levels']):
                    self.log_test("Personalization Data", True, "User profile and difficulty data included")
                else:
                    self.log_test("Personalization Data", False, "Missing personalization data")
                
                return challenge['id']
            else:
                self.log_test("Challenge Generation", False, f"Missing required fields: {missing_fields}")
        else:
            self.log_test("Challenge Generation", False, "Failed to generate challenge", message)
        
        return None

    def test_challenge_submission(self, challenge_id):
        """Test challenge submission and scoring"""
        print("\n📝 Testing Challenge Submission")
        
        # Mock responses for a quiz challenge
        mock_responses = {
            'question_0': 'option_a',
            'question_1': 'option_b',
            'difficulty_rating': 4
        }
        
        success, message, data = self.test_api_endpoint(
            'POST',
            f'/api/adaptive-challenges/{challenge_id}/submit/',
            {
                'responses': mock_responses,
                'feedback': 'Found this challenging but educational'
            }
        )
        
        if success and data.get('success'):
            score = data.get('score', 0)
            feedback = data.get('feedback', '')
            next_steps = data.get('next_steps', [])
            difficulty_adjustment = data.get('difficulty_adjustment', {})
            
            # Validate response structure
            if 0 <= score <= 1:
                self.log_test("Challenge Scoring", True, f"Score calculated: {score:.2f}")
            else:
                self.log_test("Challenge Scoring", False, f"Invalid score: {score}")
            
            if feedback:
                self.log_test("AI Feedback", True, "Personalized feedback generated")
            else:
                self.log_test("AI Feedback", False, "No feedback generated")
            
            if next_steps:
                self.log_test("Next Steps", True, f"{len(next_steps)} learning recommendations provided")
            else:
                self.log_test("Next Steps", False, "No next steps provided")
            
            if difficulty_adjustment:
                self.log_test("Difficulty Adjustment", True, f"Level: {difficulty_adjustment.get('new_difficulty', 'N/A')}")
            else:
                self.log_test("Difficulty Adjustment", False, "No difficulty adjustment information")
            
            return True
        else:
            self.log_test("Challenge Submission", False, "Failed to submit challenge", message)
            return False

    def test_performance_analytics(self):
        """Test performance analytics endpoint"""
        print("\n📊 Testing Performance Analytics")
        
        success, message, data = self.test_api_endpoint(
            'GET',
            '/api/performance/analytics/?days=30'
        )
        
        if success:
            # Validate analytics structure
            required_sections = ['performance_data', 'difficulty_metrics', 'learning_patterns', 'recommendations']
            missing_sections = [section for section in required_sections if section not in data]
            
            if not missing_sections:
                self.log_test("Analytics Structure", True, "All required data sections present")
                
                # Check difficulty metrics
                metrics = data.get('difficulty_metrics', {})
                key_metrics = ['challenge_success_rate', 'average_challenge_score', 'learning_velocity', 'engagement_level']
                missing_metrics = [metric for metric in key_metrics if metric not in metrics]
                
                if not missing_metrics:
                    self.log_test("Difficulty Metrics", True, f"Success rate: {metrics.get('challenge_success_rate', 0):.1%}")
                else:
                    self.log_test("Difficulty Metrics", False, f"Missing metrics: {missing_metrics}")
                
                # Check recommendations
                recommendations = data.get('recommendations', {})
                if 'recommendations' in recommendations and recommendations['recommendations']:
                    self.log_test("AI Recommendations", True, f"{len(recommendations['recommendations'])} recommendations generated")
                else:
                    self.log_test("AI Recommendations", False, "No recommendations generated")
                
            else:
                self.log_test("Analytics Structure", False, f"Missing sections: {missing_sections}")
        else:
            self.log_test("Performance Analytics", False, "Failed to fetch analytics", message)

    def test_difficulty_profile(self):
        """Test user difficulty profile management"""
        print("\n⚖️ Testing Difficulty Profile")
        
        # Get user difficulty profile
        success, message, profile_data = self.test_api_endpoint(
            'GET',
            '/api/difficulty-profile/'
        )
        
        if success:
            required_fields = ['current_difficulty', 'jac_knowledge_level', 'problem_solving_level', 'coding_skill_level']
            missing_fields = [field for field in required_fields if field not in profile_data]
            
            if not missing_fields:
                self.log_test("Difficulty Profile", True, f"Current level: {profile_data['current_difficulty']}")
                
                # Test analytics endpoint
                success2, message2, analytics_data = self.test_api_endpoint(
                    'GET',
                    '/api/difficulty-profile/analytics/?days=30'
                )
                
                if success2 and analytics_data.get('success'):
                    self.log_test("Difficulty Analytics", True, "Profile analytics available")
                else:
                    self.log_test("Difficulty Analytics", False, "Profile analytics failed", message2)
                
                # Test difficulty adjustment
                success3, message3, adjustment_data = self.test_api_endpoint(
                    'POST',
                    '/api/difficulty-profile/adjust-difficulty/',
                    {'adjustment_type': 'maintain'}
                )
                
                if success3:
                    self.log_test("Difficulty Adjustment", True, f"Status: {adjustment_data.get('message', 'N/A')}")
                else:
                    self.log_test("Difficulty Adjustment", False, "Adjustment failed", message3)
                
            else:
                self.log_test("Difficulty Profile", False, f"Missing profile fields: {missing_fields}")
        else:
            self.log_test("Difficulty Profile", False, "Failed to fetch profile", message)

    def test_spaced_repetition(self):
        """Test spaced repetition functionality"""
        print("\n🔄 Testing Spaced Repetition")
        
        # Get due reviews
        success, message, reviews_data = self.test_api_endpoint(
            'GET',
            '/api/adaptive-challenges/due-reviews/'
        )
        
        if success:
            reviews = reviews_data.get('reviews', [])
            
            if isinstance(reviews, list):
                self.log_test("Due Reviews", True, f"{len(reviews)} reviews ready")
                
                # If there are reviews, test the spaced repetition endpoints
                if reviews:
                    first_review = reviews[0]
                    session_id = first_review.get('session_id')
                    
                    if session_id:
                        # Test review completion
                        success2, message2, complete_data = self.test_api_endpoint(
                            'POST',
                            f'/api/spaced-repetition/{session_id}/complete-review/',
                            {'quality_rating': 4}
                        )
                        
                        if success2:
                            self.log_test("Review Completion", True, f"Next review: {complete_data.get('next_review_date', 'N/A')}")
                        else:
                            self.log_test("Review Completion", False, "Failed to complete review", message2)
                
            else:
                self.log_test("Due Reviews", False, "Invalid reviews data format")
        else:
            self.log_test("Due Reviews", False, "Failed to fetch reviews", message)

    def test_challenge_history(self):
        """Test challenge attempt history"""
        print("\n📋 Testing Challenge History")
        
        success, message, attempts_data = self.test_api_endpoint(
            'GET',
            '/api/adaptive-challenges/my-attempts/'
        )
        
        if success:
            attempts = attempts_data if isinstance(attempts_data, list) else attempts_data.get('results', [])
            
            if isinstance(attempts, list):
                self.log_test("Challenge History", True, f"{len(attempts)} attempts found")
                
                # Analyze attempt patterns
                if attempts:
                    latest_attempt = attempts[0]
                    required_fields = ['id', 'challenge', 'status', 'score', 'started_at']
                    missing_fields = [field for field in required_fields if field not in latest_attempt]
                    
                    if not missing_fields:
                        self.log_test("Attempt Records", True, "Complete attempt information available")
                    else:
                        self.log_test("Attempt Records", False, f"Missing fields: {missing_fields}")
                
            else:
                self.log_test("Challenge History", False, "Invalid attempts data format")
        else:
            self.log_test("Challenge History", False, "Failed to fetch attempts", message)

    def test_learning_recommendations(self):
        """Test learning recommendations"""
        print("\n💡 Testing Learning Recommendations")
        
        success, message, recommendations_data = self.test_api_endpoint(
            'GET',
            '/api/recommendations/challenges/'
        )
        
        if success:
            recommendations = recommendations_data.get('recommendations', [])
            user_profile = recommendations_data.get('user_profile', {})
            
            if isinstance(recommendations, list):
                self.log_test("Learning Recommendations", True, f"{len(recommendations)} recommendations generated")
                
                if user_profile and 'current_difficulty' in user_profile:
                    self.log_test("User Profile in Recommendations", True, f"Profile level: {user_profile['current_difficulty']}")
                else:
                    self.log_test("User Profile in Recommendations", False, "Missing user profile data")
                
            else:
                self.log_test("Learning Recommendations", False, "Invalid recommendations data format")
        else:
            self.log_test("Learning Recommendations", False, "Failed to fetch recommendations", message)

    def run_comprehensive_test(self):
        """Run comprehensive test suite"""
        print("🚀 Starting Adaptive Learning System Integration Test")
        print("=" * 60)
        
        start_time = time.time()
        
        # Test authentication
        authenticated = self.test_user_authentication()
        
        # Test core adaptive learning features
        challenge_id = self.test_challenge_generation()
        
        if challenge_id:
            self.test_challenge_submission(challenge_id)
        
        # Test analytics and profile management
        self.test_performance_analytics()
        self.test_difficulty_profile()
        
        # Test spaced repetition
        self.test_spaced_repetition()
        
        # Test history and recommendations
        self.test_challenge_history()
        self.test_learning_recommendations()
        
        # Print summary
        elapsed_time = time.time() - start_time
        self.print_test_summary(elapsed_time)

    def print_test_summary(self, elapsed_time):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result['success'])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {total - passed} ❌")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        print(f"Test Duration: {elapsed_time:.2f} seconds")
        
        if total - passed > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test']}: {result['message']}")
                    if result['details']:
                        print(f"    Details: {result['details']}")
        
        print("\n" + "=" * 60)
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! Adaptive Learning System is fully functional.")
        else:
            print(f"⚠️  {total - passed} tests failed. Review the implementation.")


def main():
    """Main function"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:8000"
    
    print(f"Testing Adaptive Learning System at: {base_url}")
    print("Make sure your Django backend is running with all adaptive learning endpoints available.")
    print()
    
    # Create tester instance
    tester = AdaptiveLearningTester(base_url)
    
    # Run comprehensive test
    tester.run_comprehensive_test()


if __name__ == "__main__":
    main()
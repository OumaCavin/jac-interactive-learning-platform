"""
Assessment tests for Django
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import uuid

from .models import AssessmentAttempt, AssessmentQuestion, UserAssessmentResult
from apps.learning.models import Module

User = get_user_model()


class AssessmentQuestionModelTest(TestCase):
    """
    Test cases for AssessmentQuestion model
    """
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.module = Module.objects.create(
            title='Test Module',
            description='Test module description',
            created_by=self.user
        )
        
        self.question = AssessmentQuestion.objects.create(
            module=self.module,
            title='Test Question',
            question_text='What is 2+2?',
            question_type='multiple_choice',
            difficulty='easy',
            options=['3', '4', '5', '6'],
            correct_answer='4',
            explanation='2+2 equals 4',
            points=1.0
        )
    
    def test_assessment_question_creation(self):
        """Test AssessmentQuestion model creation"""
        self.assertTrue(isinstance(self.question, AssessmentQuestion))
        self.assertEqual(str(self.question), 'Test Question (easy) - Test Module')
        self.assertEqual(self.question.question_type, 'multiple_choice')
        self.assertEqual(self.question.difficulty, 'easy')
    
    def test_assessment_question_fields(self):
        """Test AssessmentQuestion model fields"""
        self.assertEqual(self.question.title, 'Test Question')
        self.assertEqual(self.question.question_text, 'What is 2+2?')
        self.assertEqual(self.question.correct_answer, '4')
        self.assertEqual(self.question.explanation, '2+2 equals 4')
        self.assertEqual(self.question.points, 1.0)
    
    def test_question_id_is_uuid(self):
        """Test that question_id is a valid UUID"""
        self.assertTrue(isinstance(self.question.question_id, uuid.UUID))


class AssessmentAttemptModelTest(TestCase):
    """
    Test cases for AssessmentAttempt model
    """
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.module = Module.objects.create(
            title='Test Module',
            description='Test module description',
            created_by=self.user
        )
        
        self.attempt = AssessmentAttempt.objects.create(
            user=self.user,
            module=self.module,
            status='in_progress'
        )
    
    def test_assessment_attempt_creation(self):
        """Test AssessmentAttempt model creation"""
        self.assertTrue(isinstance(self.attempt, AssessmentAttempt))
        self.assertEqual(self.attempt.user, self.user)
        self.assertEqual(self.attempt.module, self.module)
        self.assertEqual(self.attempt.status, 'in_progress')
    
    def test_attempt_id_is_uuid(self):
        """Test that attempt_id is a valid UUID"""
        self.assertTrue(isinstance(self.attempt.attempt_id, uuid.UUID))
    
    def test_is_passed_property(self):
        """Test is_passed property"""
        # Test when score is None
        self.assertFalse(self.attempt.is_passed)
        
        # Test when score is below passing score
        self.attempt.score = 60
        self.attempt.passing_score = 70
        self.assertFalse(self.attempt.is_passed)
        
        # Test when score is above passing score
        self.attempt.score = 80
        self.assertTrue(self.attempt.is_passed)


class AssessmentAttemptAPITest(APITestCase):
    """
    Test cases for AssessmentAttempt API endpoints
    """
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.module = Module.objects.create(
            title='Test Module',
            description='Test module description',
            created_by=self.user
        )
        
        self.attempt = AssessmentAttempt.objects.create(
            user=self.user,
            module=self.module,
            status='completed',
            score=85.0
        )
    
    def test_create_assessment_attempt(self):
        """Test creating a new assessment attempt"""
        url = reverse('assessmentattempt-list')
        data = {
            'module': str(self.module.module_id),
            'time_limit_minutes': 60
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('attempt_id', response.data)
    
    def test_get_assessment_attempts(self):
        """Test getting assessment attempts"""
        url = reverse('assessmentattempt-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_get_specific_attempt(self):
        """Test getting a specific assessment attempt"""
        url = reverse('assessmentattempt-detail', kwargs={'pk': self.attempt.attempt_id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['score'], 85.0)
    
    def test_submit_attempt(self):
        """Test submitting an assessment attempt"""
        # Create a question for testing
        question = AssessmentQuestion.objects.create(
            module=self.module,
            title='Test Question',
            question_text='What is 2+2?',
            question_type='multiple_choice',
            correct_answer='4',
            points=1.0
        )
        
        url = reverse('assessmentattempt-submit', kwargs={'pk': self.attempt.attempt_id})
        data = {
            'answers': {str(question.question_id): '4'}
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status.status_code, status.HTTP_200_OK)


class AssessmentQuestionAPITest(APITestCase):
    """
    Test cases for AssessmentQuestion API endpoints
    """
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.module = Module.objects.create(
            title='Test Module',
            description='Test module description',
            created_by=self.user
        )
        
        self.question = AssessmentQuestion.objects.create(
            module=self.module,
            title='Test Question',
            question_text='What is 2+2?',
            question_type='multiple_choice',
            options=['3', '4', '5', '6'],
            correct_answer='4',
            explanation='2+2 equals 4',
            points=1.0
        )
    
    def test_create_question(self):
        """Test creating a new question"""
        url = reverse('assessmentquestion-list')
        data = {
            'module': str(self.module.module_id),
            'title': 'New Question',
            'question_text': 'What is 3+3?',
            'question_type': 'multiple_choice',
            'options': ['5', '6', '7', '8'],
            'correct_answer': '6',
            'explanation': '3+3 equals 6',
            'points': 1.0
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('question_id', response.data)
    
    def test_get_questions(self):
        """Test getting questions"""
        url = reverse('assessmentquestion-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_check_answer(self):
        """Test checking if an answer is correct"""
        url = reverse('assessmentquestion-check-answer', kwargs={'pk': self.question.question_id})
        data = {
            'question_id': str(self.question.question_id),
            'answer': '4'
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_correct'])


class UserAssessmentResultTest(TestCase):
    """
    Test cases for UserAssessmentResult model
    """
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.module = Module.objects.create(
            title='Test Module',
            description='Test module description',
            created_by=self.user
        )
        
        self.result = UserAssessmentResult.objects.create(
            user=self.user,
            module=self.module,
            result_type='module_completion',
            total_attempts=3,
            best_score=85.0,
            average_score=75.5
        )
    
    def test_user_assessment_result_creation(self):
        """Test UserAssessmentResult model creation"""
        self.assertTrue(isinstance(self.result, UserAssessmentResult))
        self.assertEqual(self.result.result_type, 'module_completion')
        self.assertEqual(self.result.total_attempts, 3)
        self.assertEqual(self.result.best_score, 85.0)
        self.assertEqual(self.result.average_score, 75.5)
    
    def test_result_id_is_uuid(self):
        """Test that result_id is a valid UUID"""
        self.assertTrue(isinstance(self.result.result_id, uuid.UUID))


class AssessmentIntegrationTest(TestCase):
    """
    Integration tests for assessment functionality
    """
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.module = Module.objects.create(
            title='Test Module',
            description='Test module description',
            created_by=self.user
        )
        
        # Create sample questions
        self.question1 = AssessmentQuestion.objects.create(
            module=self.module,
            title='Question 1',
            question_text='What is 2+2?',
            question_type='multiple_choice',
            options=['3', '4', '5', '6'],
            correct_answer='4',
            points=2.0
        )
        
        self.question2 = AssessmentQuestion.objects.create(
            module=self.module,
            title='Question 2',
            question_text='What is 3+3?',
            question_type='multiple_choice',
            options=['5', '6', '7', '8'],
            correct_answer='6',
            points=3.0
        )
    
    def test_complete_assessment_workflow(self):
        """Test complete assessment workflow"""
        # 1. Create assessment attempt
        attempt = AssessmentAttempt.objects.create(
            user=self.user,
            module=self.module,
            status='in_progress'
        )
        
        # 2. Submit answers
        answers = {
            str(self.question1.question_id): '4',
            str(self.question2.question_id): '6'
        }
        
        # 3. Calculate score
        total_points = self.question1.points + self.question2.points  # 2.0 + 3.0 = 5.0
        expected_score = (5.0 / total_points) * 100  # 100%
        
        # 4. Update attempt
        attempt.answers = answers
        attempt.score = expected_score
        attempt.status = 'completed'
        attempt.completed_at = attempt.started_at  # Simplified for test
        attempt.save()
        
        # 5. Verify results
        self.assertEqual(attempt.score, 100.0)
        self.assertTrue(attempt.is_passed)
        self.assertEqual(attempt.status, 'completed')
    
    def test_average_score_property(self):
        """Test Module's average_score property"""
        # Create some assessment attempts with scores
        AssessmentAttempt.objects.create(
            user=self.user,
            module=self.module,
            status='completed',
            score=80.0
        )
        
        AssessmentAttempt.objects.create(
            user=self.user,
            module=self.module,
            status='completed',
            score=90.0
        )
        
        # Test average score calculation
        expected_avg = (80.0 + 90.0) / 2  # 85.0
        actual_avg = self.module.average_score
        
        self.assertEqual(actual_avg, expected_avg)
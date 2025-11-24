# Backend API Specification for JAC Learning Platform

## Overview
This document outlines all the backend APIs and integrations required to make the frontend application fully functional. The frontend is currently using mock data and needs real backend endpoints.

## Base Configuration
- **Base URL**: `http://localhost:8000/api` (configurable via `REACT_APP_API_URL`)
- **Authentication**: JWT Bearer tokens (`Authorization: Bearer <token>`)
- **Content-Type**: `application/json`
- **Response Format**: JSON

---

## 1. AUTHENTICATION SERVICE APIs

### 1.1 User Registration
```http
POST /users/auth/register/
Content-Type: application/json

{
  "username": "string",
  "email": "string",
  "password": "string",
  "password_confirm": "string",
  "first_name": "string?",
  "last_name": "string?"
}

Response:
{
  "user": {
    "id": "string",
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "is_staff": "boolean",
    "bio": "string?",
    "profile_image": "string?",
    "learning_style": "visual|auditory|kinesthetic|reading",
    "preferred_difficulty": "beginner|intermediate|advanced",
    "learning_pace": "slow|moderate|fast",
    "total_modules_completed": "number",
    "total_time_spent": "string",
    "current_streak": "number",
    "longest_streak": "number",
    "total_points": "number",
    "level": "number",
    "experience_level": "number",
    "next_level_points": "number",
    "achievements": "array",
    "badges": "array",
    "current_goal": "string?",
    "goal_deadline": "string?",
    "agent_interaction_level": "minimal|moderate|high",
    "preferred_feedback_style": "detailed|brief|encouraging",
    "dark_mode": "boolean",
    "notifications_enabled": "boolean",
    "email_notifications": "boolean",
    "push_notifications": "boolean",
    "created_at": "string",
    "updated_at": "string"
  },
  "tokens": {
    "access": "string",
    "refresh": "string"
  }
}
```

### 1.2 User Login
```http
POST /users/auth/login/
Content-Type: application/json

{
  "username": "string",
  "password": "string"
}

Response: Same as registration
```

### 1.3 Token Refresh
```http
POST /users/auth/refresh/
Content-Type: application/json

{
  "refresh": "string"
}

Response:
{
  "access": "string"
}
```

### 1.4 User Logout
```http
POST /users/auth/logout/
Content-Type: application/json
Authorization: Bearer <refresh_token>

{
  "refresh": "string"
}
```

### 1.5 Profile Management
```http
GET /users/profile/
Authorization: Bearer <access_token>

PUT /users/profile/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  // Partial user data as shown above
}
```

### 1.6 Settings Management
```http
GET /users/settings/
Authorization: Bearer <access_token>

PUT /users/settings/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "learning_style": "visual|auditory|kinesthetic|reading",
  "preferred_difficulty": "beginner|intermediate|advanced",
  "learning_pace": "slow|moderate|fast",
  "dark_mode": "boolean",
  "notifications_enabled": "boolean",
  "email_notifications": "boolean",
  "push_notifications": "boolean",
  "current_goal": "string?",
  "goal_deadline": "string?",
  "agent_interaction_level": "minimal|moderate|high",
  "preferred_feedback_style": "detailed|brief|encouraging"
}
```

### 1.7 User Analytics
```http
GET /users/learning-summary/
Authorization: Bearer <access_token>

GET /users/stats/
Authorization: Bearer <access_token>
```

### 1.8 Password Management
```http
POST /auth/password-reset/
Content-Type: application/json

{
  "email": "string"
}

POST /auth/password-reset/confirm/
Content-Type: application/json

{
  "token": "string",
  "password": "string"
}

POST /auth/password-change/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "current_password": "string",
  "new_password": "string"
}
```

---

## 2. AGENT SERVICE APIs

### 2.1 Agent Management
```http
GET /agents/
Authorization: Bearer <access_token>

Response: [
  {
    "id": "number",
    "name": "string",
    "type": "code_evaluator|learning_coordinator|content_generator|progress_tracker|chat_assistant|knowledge_graph",
    "status": "idle|busy|error",
    "current_task": "string|null",
    "performance_metrics": {
      "tasks_completed": "number",
      "average_response_time": "number",
      "success_rate": "number"
    },
    "capabilities": ["string"],
    "created_at": "string"
  }
]

GET /agents/{id}/
Authorization: Bearer <access_token>

POST /agents/
Authorization: Bearer <access_token>
Content-Type: application/json

PATCH /agents/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

DELETE /agents/{id}/
Authorization: Bearer <access_token>
```

### 2.2 Task Management
```http
GET /tasks/
Authorization: Bearer <access_token>
Query: ?agent={agent_id}

Response: [
  {
    "id": "number",
    "agent": "number",
    "title": "string",
    "description": "string",
    "status": "pending|in_progress|completed|failed",
    "priority": "low|medium|high|urgent",
    "input_data": "object",
    "output_data": "object",
    "created_at": "string",
    "started_at": "string|null",
    "completed_at": "string|null",
    "estimated_duration": "number",
    "actual_duration": "number|null"
  }
]

GET /tasks/{id}/
Authorization: Bearer <access_token>

POST /tasks/
Authorization: Bearer <access_token>
Content-Type: application/json

PATCH /tasks/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json
```

### 2.3 Agent Actions
```http
POST /agents/code-evaluator/evaluate/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "code": "string",
  "language": "python|jac",
  "test_cases": ["object"]
}

POST /agents/content-generator/generate/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "topic": "string",
  "difficulty": "string",
  "learning_style": "string?"
}

POST /agents/progress-tracker/track/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "user_id": "number",
  "module_id": "number",
  "progress_data": "object"
}
```

### 2.4 Chat Assistant
```http
POST /agents/chat-assistant/message/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "message": "string",
  "session_id": "string?"
}

Response:
{
  "id": "number",
  "agent": "number",
  "user": "number",
  "message": "string",
  "response": "string",
  "session_id": "string",
  "created_at": "string",
  "feedback_rating": "number|null"
}

GET /agents/chat-assistant/history/
Authorization: Bearer <access_token>
Query: ?session_id={session_id}

POST /agents/chat-assistant/rate/{message_id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "rating": "number"
}
```

### 2.5 Knowledge Graph
```http
GET /agents/knowledge-graph/
Authorization: Bearer <access_token>
Query: ?topic={topic}

GET /agents/knowledge-graph/relations/
Authorization: Bearer <access_token>
Query: ?concept={concept}
```

### 2.6 Metrics and Analytics
```http
GET /agents/metrics/
Authorization: Bearer <access_token>

GET /agents/{agent_id}/metrics/
Authorization: Bearer <access_token>

GET /agents/system-metrics/
Authorization: Bearer <access_token>

GET /agents/status/
Authorization: Bearer <access_token>

POST /agents/{agent_id}/restart/
Authorization: Bearer <access_token>

GET /agents/{agent_id}/logs/
Authorization: Bearer <access_token>
Query: ?limit={number}
```

### 2.7 Learning Coordinator
```http
POST /agents/learning-coordinator/recommend/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "user_id": "number"
}

POST /agents/learning-coordinator/progress/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "user_id": "number",
  "module_id": "number",
  "completion_data": "object"
}
```

---

## 3. LEARNING SERVICE APIs

### 3.1 Learning Paths
```http
GET /learning/learning-paths/
Authorization: Bearer <access_token>

Response: [
  {
    "id": "number",
    "title": "string",
    "description": "string",
    "difficulty_level": "beginner|intermediate|advanced",
    "estimated_duration": "number",
    "modules_count": "number",
    "rating": "number",
    "created_at": "string",
    "updated_at": "string"
  }
]

GET /learning/learning-paths/{id}/
Authorization: Bearer <access_token>
```

### 3.2 Modules
```http
GET /learning/modules/
Authorization: Bearer <access_token>
Query: ?learning_path={path_id}

Response: [
  {
    "id": "number",
    "learning_path": "number",
    "title": "string",
    "description": "string",
    "content": "string",
    "order_index": "number",
    "estimated_duration": "number",
    "module_type": "lesson|exercise|assessment",
    "prerequisites": ["number"],
    "created_at": "string",
    "updated_at": "string"
  }
]

GET /learning/modules/{id}/
Authorization: Bearer <access_token>
```

### 3.3 Code Execution
```http
POST /learning/code/execute/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "code": "string",
  "language": "python|jac",
  "test_input": "string?",
  "timeout": "number?",
  "memory_limit": "number?"
}

Response:
{
  "success": "boolean",
  "output": "string",
  "execution_time": "number",
  "memory_usage": "number",
  "error": "string?"
}
```

### 3.4 Code Submissions
```http
POST /learning/code-submissions/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "user": "number",
  "module": "number",
  "code": "string",
  "language": "python|jac"
}

GET /learning/code-submissions/{id}/
Authorization: Bearer <access_token>

GET /learning/code-submissions/
Authorization: Bearer <access_token>
Query: ?user={user_id}&module={module_id}

PATCH /learning/code-submissions/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json
```

### 3.5 User Progress
```http
GET /learning/user-module-progress/
Authorization: Bearer <access_token>
Query: ?user={user_id}&module={module_id}

Response:
{
  "id": "number",
  "user": "number",
  "module": "number",
  "status": "not_started|in_progress|completed",
  "time_spent": "number",
  "attempts": "number",
  "score": "number",
  "last_accessed": "string",
  "completed_at": "string|null"
}

PATCH /learning/user-module-progress/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "status": "not_started|in_progress|completed",
  "time_spent": "number",
  "score": "number"
}
```

### 3.6 AI Code Review
```http
GET /learning/ai-code-reviews/
Authorization: Bearer <access_token>
Query: ?submission={submission_id}

POST /learning/ai-code-reviews/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "submission": "number",
  "code": "string",
  "review": "object"
}
```

### 3.7 Test Cases
```http
GET /learning/test-cases/
Authorization: Bearer <access_token>
Query: ?module={module_id}

Response: [
  {
    "id": "number",
    "module": "number",
    "input": "string",
    "expected_output": "string",
    "points": "number"
  }
]
```

### 3.8 Admin Analytics
```http
GET /learning/admin/analytics/
Authorization: Bearer <access_token>
Query: ?path_id={path_id}

GET /learning/admin/completion-trends/
Authorization: Bearer <access_token>
Query: ?timeframe={week|month|quarter|year}

GET /learning/admin/user-journey/
Authorization: Bearer <access_token>
Query: ?path_id={path_id}

GET /learning/admin/insights/
Authorization: Bearer <access_token>

PATCH /learning/learning-paths/bulk-update/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "path_ids": ["number"],
  "updates": "object"
}

POST /learning/learning-paths/{path_id}/reorder-modules/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "module_order": ["number"]
}
```

---

## 4. ASSESSMENT SERVICE APIs

### 4.1 Quiz Management
```http
GET /assessment/quizzes/
Authorization: Bearer <access_token>

Response: [
  {
    "id": "string",
    "title": "string",
    "description": "string",
    "learning_path": "string?",
    "module": "string?",
    "difficulty": "easy|medium|hard",
    "time_limit": "number?",
    "max_attempts": "number",
    "passing_score": "number",
    "questions": [
      {
        "id": "string",
        "type": "multiple_choice|true_false|short_answer|code_completion|jac_specific",
        "question": "string",
        "options": ["string"]?,
        "correct_answer": "string|string[]",
        "explanation": "string?",
        "jac_concept": "string?",
        "difficulty": "1|2|3|4|5",
        "points": "number"
      }
    ],
    "created_at": "string",
    "updated_at": "string"
  }
]

GET /assessment/quizzes/{id}/
Authorization: Bearer <access_token>

POST /assessment/quizzes/
Authorization: Bearer <access_token>
Content-Type: application/json

PATCH /assessment/quizzes/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

DELETE /assessment/quizzes/{id}/
Authorization: Bearer <access_token>
```

### 4.2 Quiz Attempts
```http
GET /assessment/attempts/
Authorization: Bearer <access_token>
Query: ?quiz={quiz_id}&user={user_id}

Response: [
  {
    "id": "string",
    "quiz": "string",
    "user": "string",
    "answers": {
      "question_id": "string|string[]"
    },
    "score": "number",
    "max_score": "number",
    "passed": "boolean",
    "time_taken": "number",
    "started_at": "string",
    "completed_at": "string?",
    "feedback": "string?"
  }
]

POST /assessment/attempts/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "quiz": "string",
  "answers": {
    "question_id": "string|string[]"
  },
  "time_taken": "number"
}

GET /assessment/attempts/{id}/
Authorization: Bearer <access_token>

PATCH /assessment/attempts/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json
```

### 4.3 Analytics and Performance
```http
GET /assessment/analytics/performance/
Authorization: Bearer <access_token>
Query: ?quiz_id={quiz_id}&timeframe={week|month|quarter|year}

GET /assessment/analytics/score-distribution/
Authorization: Bearer <access_token>
Query: ?quiz_id={quiz_id}

GET /assessment/analytics/time-analysis/
Authorization: Bearer <access_token>
Query: ?quiz_id={quiz_id}
```

---

## 5. ERROR HANDLING

### Standard Error Response Format
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": "Additional error details"
  }
}
```

### Common HTTP Status Codes
- `200 OK` - Success
- `201 Created` - Resource created
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error

---

## 6. RATE LIMITING

- **Default**: 1000 requests per hour per user
- **Authentication endpoints**: 5 requests per minute
- **Code execution**: 10 requests per minute

---

## 7. WEBHOOKS (Optional)

For real-time features, consider implementing webhooks for:
- Agent status changes
- Task completions
- New messages in chat
- Quiz submissions
- Progress updates

---

## 8. TESTING ENDPOINTS

```http
GET /health/
GET /api/docs/  # Swagger/OpenAPI documentation
GET /api/version/  # API version information
```

---

## 9. IMPLEMENTATION PRIORITY

### Phase 1 (High Priority)
1. Authentication Service APIs
2. Basic Learning Path and Module APIs
3. Basic Agent Management APIs
4. Chat Assistant APIs

### Phase 2 (Medium Priority)
1. Code Execution APIs
2. User Progress Tracking
3. Assessment APIs
4. Advanced Agent Actions

### Phase 3 (Low Priority)
1. Analytics and Reporting APIs
2. Admin Management APIs
3. Advanced Features

---

## 10. DEVELOPMENT NOTES

- Use proper HTTP status codes
- Implement proper validation
- Add request/response logging
- Use database transactions for data integrity
- Implement caching for frequently accessed data
- Add proper indexing for performance
- Use environment variables for configuration
- Implement proper error logging and monitoring
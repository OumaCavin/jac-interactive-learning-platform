# JAC Learning Platform - Testing Guide

## Quick Start (Post-Migration Fix)

### 1. Fix Django Migration Issue
```bash
cd backend
python manage.py migrate
python manage.py populate_jac_curriculum
python manage.py runserver
```

### 2. Test AI Chat Functionality
1. Navigate to `http://localhost:8000/chat`
2. Select an AI agent from the sidebar
3. Send messages like:
   - "What is JAC programming?"
   - "Explain Object-Spatial Programming"
   - "Help me understand nodes and edges"
   - "Give me a coding exercise"

### 3. Test Code Editor
1. Navigate to `http://localhost:8000/code-editor`
2. Select "JAC (Jaseci)" language
3. Try sample code:
```jac
walker test_walker {
    can print;
    print("Hello from JAC!");
    
    node person {
        has name, age;
    }
    
    person_1 = spawn node.person(name="Alice", age=25);
    report {"message": "JAC execution completed!"};
}
```
4. Click "Run Code" or press Ctrl+Enter

### 4. Test Learning Curriculum
1. Navigate to `http://localhost:8000/learning`
2. Browse the populated JAC curriculum
3. Complete lessons and exercises
4. Track progress through the dashboard

## API Endpoints to Test

### Chat API
```bash
curl -X POST http://localhost:8000/agents/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "What is JAC programming?", "session_id": "test-session"}'
```

### JAC Execution API
```bash
curl -X POST http://localhost:8000/jac-execution/api/quick-execute/ \
  -H "Content-Type: application/json" \
  -d '{"code": "walker hello { can print; print(\"Hello JAC!\"); }", "language": "jac"}'
```

## Expected Behavior

### Chat System
- AI responds with JAC-specific expertise
- Maintains conversation context
- Provides learning guidance and explanations
- Handles errors gracefully

### Code Editor
- Executes JAC code securely in sandbox
- Shows execution time and memory usage
- Displays output and any errors
- Provides syntax validation

### Learning Content
- 44 lessons across 5 modules
- Interactive exercises and assessments
- Progress tracking and analytics
- Comprehensive JAC curriculum

## Troubleshooting

### If Chat Doesn't Work
- Check if OpenAI API key is set in environment
- Verify backend server is running
- Check browser console for errors

### If Code Execution Fails
- Ensure JAC interpreter is available
- Check security sandbox settings
- Verify code syntax is valid

### If Learning Content Missing
- Run `python manage.py populate_jac_curriculum`
- Check database connectivity
- Verify model migrations are applied
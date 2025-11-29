# Manual Fix Instructions for Admin Access Issue

Since git sync failed, here are the exact changes you need to make manually to each admin.py file:

## Files to Update (9 total)

### 1. backend/apps/users/admin.py
```python
# Add this import after the existing imports:
from config.custom_admin import custom_admin_site

# Change this line:
@admin.register(User)

# To this:
@admin.register(User, site=custom_admin_site)
```

### 2. backend/apps/assessments/admin.py
```python
# Add this import after the existing imports:
from config.custom_admin import custom_admin_site

# Change all @admin.register lines to include site=custom_admin_site
@admin.register(AssessmentQuestion, site=custom_admin_site)
@admin.register(AssessmentAttempt, site=custom_admin_site)
@admin.register(UserAssessmentResult, site=custom_admin_site)
```

### 3. backend/apps/collaboration/admin.py
```python
# Add this import after the existing imports:
from config.custom_admin import custom_admin_site

# Change all @admin.register lines to include site=custom_admin_site
@admin.register(StudyGroup, site=custom_admin_site)
@admin.register(StudyGroupMembership, site=custom_admin_site)
# ... etc for all models in this file
```

### 4. backend/apps/content/admin.py
```python
# Add this import after the existing imports:
from config.custom_admin import custom_admin_site

# Change all @admin.register lines to include site=custom_admin_site
@admin.register(Content, site=custom_admin_site)
@admin.register(ContentRecommendation, site=custom_admin_site)
@admin.register(ContentAnalytics, site=custom_admin_site)
```

### 5. backend/apps/gamification/admin.py
```python
# Add this import after the existing imports:
from config.custom_admin import custom_admin_site

# Change all @admin.register lines to include site=custom_admin_site
@admin.register(Badge, site=custom_admin_site)
@admin.register(UserBadge, site=custom_admin_site)
# ... etc for all models in this file
```

### 6. backend/apps/jac_execution/admin.py
```python
# Add this import after the existing imports:
from config.custom_admin import custom_admin_site

# Change all @admin.register lines to include site=custom_admin_site
@admin.register(CodeExecution, site=custom_admin_site)
@admin.register(ExecutionTemplate, site=custom_admin_site)
# ... etc for all models in this file
```

### 7. backend/apps/knowledge_graph/admin.py
```python
# Add this import after the existing imports:
from config.custom_admin import custom_admin_site

# Change all @admin.register lines to include site=custom_admin_site
@admin.register(KnowledgeNode, site=custom_admin_site)
@admin.register(KnowledgeEdge, site=custom_admin_site)
# ... etc for all models in this file
```

### 8. backend/apps/learning/admin.py
```python
# Add this import after the existing imports:
from config.custom_admin import custom_admin_site

# Change all @admin.register lines to include site=custom_admin_site
@admin.register(LearningPath, site=custom_admin_site)
@admin.register(Module, site=custom_admin_site)
# ... etc for all models in this file
```

### 9. backend/search/admin.py
```python
# Add this import after the existing imports:
from config.custom_admin import custom_admin_site

# Change all @admin.register lines to include site=custom_admin_site
@admin.register(SearchQuery, site=custom_admin_site)
@admin.register(SearchResult, site=custom_admin_site)
```

## Quick Method for Each File

1. **Open each admin.py file**
2. **Add the import:** `from config.custom_admin import custom_admin_site`
3. **Find all lines starting with `@admin.register`**
4. **Add `, site=custom_admin_site` to each `@admin.register(...)` line**

## Example Before and After

**Before:**
```python
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ...
```

**After:**
```python
from config.custom_admin import custom_admin_site

@admin.register(User, site=custom_admin_site)
class UserAdmin(BaseUserAdmin):
    ...
```

## After Making Changes

1. **Restart the backend:** `docker-compose restart backend`
2. **Verify:** `docker-compose exec backend python manage.py verify_admin_setup`
3. **Test:** Go to `http://localhost:8000/admin/` and login with "Ouma"

This should resolve the "Access Denied" error completely!
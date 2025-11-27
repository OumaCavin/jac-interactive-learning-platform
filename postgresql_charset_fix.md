# PostgreSQL Charset Fix

## Problem
PostgreSQL doesn't support the `charset` connection option (that's MySQL only).

## Solution
Remove the `charset` option from database settings.

### File to Edit
`backend/config/settings.py`

### Current (Broken) Lines 109-111:
```python
'OPTIONS': {
    'charset': 'utf8',
},
```

### Fixed Version:
```python
'OPTIONS': {
    # PostgreSQL handles encoding through LC_ settings, not connection options
},
```

### Complete Fixed Database Config (Lines 101-114):
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='jac_learning_db'),
        'USER': config('DB_USER', default='jac_user'),
        'PASSWORD': config('DB_PASSWORD', default='jac_password'),
        'HOST': config('DB_HOST', default='postgres'),
        'PORT': config('DB_PORT', default='5432'),
        'OPTIONS': {
            # PostgreSQL handles encoding through LC_ settings, not connection options
        },
        'CONN_MAX_AGE': 60,
    }
}
```
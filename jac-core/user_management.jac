"""
User Management Module for Jeseci Learning Platform
Handles user registration, authentication, and profile management
"""

import jac-core::user_data_models;

# User Management Walker
walker user_management {
    can register_user;
    can authenticate_user;
    can update_user_profile;
    can get_user_progress;
    can manage_learning_preferences;
}

node user {
    has user_id: str;
    has username: str;
    has email: str;
    has registration_date: datetime;
    has learning_level: str;  # beginner, intermediate, advanced
    has preferred_learning_style: str;  # visual, auditory, kinesthetic
    has current_concepts: list;
    has mastery_scores: dict;
    has learning_streak: int;
    has achievements: list;
    
    can get_comprehensive_profile;
    can update_mastery_level;
    can track_learning_activity;
}

node learning_session {
    has session_id: str;
    has start_time: datetime;
    has end_time: datetime;
    has activities_completed: list;
    has concepts_practiced: list;
    has mastery_improvements: dict;
    
    can calculate_session_score;
    can generate_session_report;
}

# User Registration Walker
walker register_user(user_data: dict) -> dict {
    # Create new user node
    user_node = spawn node::user(
        user_id=generate_user_id(),
        username=user_data["username"],
        email=user_data["email"],
        registration_date=datetime.now(),
        learning_level=user_data.get("learning_level", "beginner"),
        preferred_learning_style=user_data.get("learning_style", "visual"),
        current_concepts=[],
        mastery_scores={},
        learning_streak=0,
        achievements=[]
    );
    
    report {
        "user_id": user_node.user_id,
        "username": user_node.username,
        "status": "registered",
        "message": "User registered successfully"
    };
}

# User Authentication Walker
walker authenticate_user(username: str, password: str) -> dict {
    # Find user by username
    users = node::user.select("username").filter_by("username", username);
    
    if users.length == 0 {
        report {"status": "error", "message": "User not found"};
    }
    
    user = users[0];
    
    # Verify password (simplified)
    if verify_password(user, password) {
        report {
            "status": "authenticated",
            "user_id": user.user_id,
            "username": user.username,
            "message": "Authentication successful"
        };
    } else {
        report {"status": "error", "message": "Invalid credentials"};
    }
}

# Profile Management Walker
walker update_user_profile(user_id: str, updates: dict) -> dict {
    user = get_user_by_id(user_id);
    
    # Update allowed fields
    for key in ["learning_level", "preferred_learning_style"] {
        if key in updates {
            user[key] = updates[key];
        }
    }
    
    report {
        "status": "updated",
        "user_id": user.user_id,
        "updates": updates,
        "message": "Profile updated successfully"
    };
}

# Progress Tracking Walker
walker get_user_progress(user_id: str) -> dict {
    user = get_user_by_id(user_id);
    
    progress_data = {
        "user_id": user.user_id,
        "current_concepts": user.current_concepts,
        "mastery_scores": user.mastery_scores,
        "learning_streak": user.learning_streak,
        "achievements": user.achievements,
        "learning_level": user.learning_level
    };
    
    report progress_data;
}

# Helper Functions
can generate_user_id() -> str {
    return "user_" + str(uuid.uuid4())[:8];
}

can verify_password(user: node, password: str) -> bool {
    # Simplified password verification
    return true;  # In real implementation, use proper hashing
}

can get_user_by_id(user_id: str) -> node {
    return node::user.select("user_id").filter_by("user_id", user_id).first();
}
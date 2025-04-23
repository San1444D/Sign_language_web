from flask import request
from datetime import datetime
from typing import TypedDict, Optional, List
import numpy as np

def get_user_ip():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip and ',' in ip:
        ip = ip.split(',')[0].strip()
    return ip

def extract_keypoints(results):
    pose = np.array([[res['x'], res['y'], res['z'], res['visibility']] for res in results['pose_landmarks']]).flatten() if results['pose_landmarks'] else np.zeros(33*4)
    face = np.array([[res['x'], res['y'], res['z']] for res in results['face_landmarks']]).flatten() if results['face_landmarks'] else np.zeros(468*3)
    lh = np.array([[res['x'], res['y'], res['z']] for res in results['left_hand_landmarks']]).flatten() if results['left_hand_landmarks'] else np.zeros(21*3)
    rh = np.array([[res['x'], res['y'], res['z']] for res in results['right_hand_landmarks']]).flatten() if results['right_hand_landmarks'] else np.zeros(21*3)
    return np.concatenate([pose, face, lh, rh])


class UserProfile(TypedDict):
    """
    User profile data structure
    """
    # Required fields
    uid: str                    # Firebase Auth UID
    email: str                  # User's email address
    display_name: str           # User's display name
    created_at: datetime        # Account creation timestamp
    
    # Optional profile fields
    avatar_url: Optional[str]   # Profile picture URL
    phone_number: Optional[str] # Contact number
    bio: Optional[str]         # User biography/description
    
    # Application specific fields
    is_active: bool            # Account status
    last_login: datetime       # Last login timestamp
    role: str                  # User role (admin/user/teacher)
    
    # Learning progress
    completed_lessons: List[str]    # List of completed lesson IDs
    practice_sessions: int          # Number of practice sessions
    accuracy_rate: float           # Overall accuracy in exercises
    
    # Settings and preferences
    notification_settings: dict     # User notification preferences
    language_preference: str        # UI language preference
    accessibility_settings: dict    # Accessibility configurations
    
    # Metadata
    updated_at: datetime           # Last profile update timestamp
    device_info: dict             # Last used device information
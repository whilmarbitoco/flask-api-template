import bleach
import re

def sanitize_string(value):
    """Remove HTML tags and dangerous characters from string input"""
    if not isinstance(value, str):
        return value
    # Remove HTML tags
    cleaned = bleach.clean(value, tags=[], strip=True)
    # Remove potential SQL injection patterns (basic protection, SQLAlchemy handles the rest)
    cleaned = re.sub(r'[;\'"\\]', '', cleaned)
    return cleaned.strip()

def sanitize_dict(data):
    """Recursively sanitize all string values in a dictionary"""
    if not isinstance(data, dict):
        return data
    
    sanitized = {}
    for key, value in data.items():
        if isinstance(value, str):
            sanitized[key] = sanitize_string(value)
        elif isinstance(value, dict):
            sanitized[key] = sanitize_dict(value)
        elif isinstance(value, list):
            sanitized[key] = [sanitize_dict(item) if isinstance(item, dict) else sanitize_string(item) if isinstance(item, str) else item for item in value]
        else:
            sanitized[key] = value
    return sanitized

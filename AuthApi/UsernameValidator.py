

class UsernameValidator:
    def __init__(self):
        pass

    def validate_username(self, username):
        # Must be at least 3 characters
        if len(username) < 3:
            return False
        
        # Must be at most 20 characters
        if len(username) > 20:
            return False
        
        # Must be alphanumeric
        if not username.isalnum():
            return False

        return True

import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class PasswordStrengthValidator:
    """
    Validate password strength with multiple criteria
    """
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        errors = []
        
        if len(password) < self.min_length:
            errors.append(
                _('Password must be at least %(min_length)d characters long.') % {
                    'min_length': self.min_length
                }
            )
        
        if not re.search(r'[A-Z]', password):
            errors.append(_('Password must contain at least one uppercase letter.'))
        
        if not re.search(r'[a-z]', password):
            errors.append(_('Password must contain at least one lowercase letter.'))
        
        if not re.search(r'\d', password):
            errors.append(_('Password must contain at least one digit.'))
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append(_('Password must contain at least one special character.'))
        
        # Check if password contains common patterns
        common_patterns = [
            r'123456', r'password', r'qwerty', r'abc123',
            r'111111', r'000000', r'admin', r'letmein'
        ]
        
        for pattern in common_patterns:
            if re.search(pattern, password.lower()):
                errors.append(_('Password contains common patterns that are not allowed.'))
                break
        
        # Check against user information if available
        if user:
            user_info = [
                user.username.lower() if user.username else '',
                user.email.lower().split('@')[0] if user.email else '',
                user.first_name.lower() if user.first_name else '',
                user.last_name.lower() if user.last_name else ''
            ]
            
            for info in user_info:
                if info and len(info) > 2 and info in password.lower():
                    errors.append(_('Password cannot contain your personal information.'))
                    break
        
        if errors:
            raise ValidationError(errors)

    def get_help_text(self):
        return _(
            'Your password must be at least %(min_length)d characters long, '
            'contain uppercase and lowercase letters, numbers, and special characters.'
        ) % {'min_length': self.min_length}

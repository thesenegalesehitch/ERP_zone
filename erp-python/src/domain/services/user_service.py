"""
User Domain Service
Business logic related to users.

Author: Alexandre Albert Ndour
"""

from typing import Optional, List
import uuid


class UserDomainService:
    """
    Domain service containing user-related business logic.
    
    This service handles operations that involve multiple entities
    or complex business rules.
    """
    
    def __init__(self):
        pass
    
    def can_assign_role(
        self,
        assigning_user_roles: List[str],
        target_role_level: int,
        assigning_user_level: int
    ) -> bool:
        """
        Check if a user can assign a role to another user.
        
        Rules:
        - Superusers can assign any role
        - Users can only assign roles with lower or equal level
        """
        return assigning_user_level > target_role_level
    
    def calculate_effective_permissions(
        self,
        user_permissions: List[str],
        role_permissions: List[str]
    ) -> List[str]:
        """
        Calculate effective permissions from user and role permissions.
        
        Permissions are combined, with user-specific permissions
        taking precedence.
        """
        combined = set(role_permissions)
        combined.update(user_permissions)
        
        # Handle wildcard
        if "*" in combined:
            return ["*"]
        
        return sorted(list(combined))
    
    def should_force_password_change(
        self,
        last_password_change,
        max_days_without_change: int = 90
    ) -> bool:
        """Check if user should be forced to change password."""
        from datetime import datetime, timedelta, timezone
        
        if last_password_change is None:
            return True
        
        if isinstance(last_password_change, datetime):
            if last_password_change.tzinfo is None:
                last_password_change = last_password_change.replace(tzinfo=timezone.utc)
        else:
            return True
        
        days_since_change = (datetime.now(timezone.utc) - last_password_change).days
        return days_since_change >= max_days_without_change
    
    def validate_user_status_for_login(
        self,
        is_active: bool,
        is_locked: bool,
        is_verified: bool
    ) -> tuple[bool, str]:
        """
        Validate if user can log in.
        
        Returns:
            Tuple of (can_login, reason)
        """
        if not is_active:
            return False, "Account is deactivated"
        
        if is_locked:
            return False, "Account is locked"
        
        if not is_verified:
            return False, "Email not verified"
        
        return True, ""
    
    def get_account_recovery_info(
        self,
        failed_attempts: int,
        locked_until,
        last_login
    ) -> dict:
        """Get account recovery information."""
        from datetime import datetime, timedelta, timezone
        
        info = {
            "failed_attempts": failed_attempts,
            "is_locked": False,
            "lock_time_remaining": None,
            "last_login": last_login,
            "recovery_actions": []
        }
        
        if locked_until:
            if isinstance(locked_until, datetime):
                if locked_until.tzinfo is None:
                    locked_until = locked_until.replace(tzinfo=timezone.utc)
                
                if datetime.now(timezone.utc) < locked_until:
                    info["is_locked"] = True
                    remaining = locked_until - datetime.now(timezone.utc)
                    info["lock_time_remaining"] = int(remaining.total_seconds())
        
        if failed_attempts > 0:
            info["recovery_actions"].append(
                "Wait for lockout to expire"
            )
        
        return info

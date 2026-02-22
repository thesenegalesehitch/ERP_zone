"""
Permission Domain Service
Business logic related to permissions and authorization.

Author: Alexandre Albert Ndour
"""

from typing import List, Set


class PermissionDomainService:
    """
    Domain service containing permission-related business logic.
    """
    
    def __init__(self):
        pass
    
    def check_permission(
        self,
        user_permissions: List[str],
        required_permission: str
    ) -> bool:
        """
        Check if user has required permission.
        
        Handles wildcard permissions.
        """
        # Check for wildcard
        if "*" in user_permissions:
            return True
        
        # Exact match
        if required_permission in user_permissions:
            return True
        
        # Check resource wildcard (e.g., "users.*" matches "users.read")
        parts = required_permission.split(".")
        if len(parts) == 2:
            resource_wildcard = f"{parts[0]}.*"
            if resource_wildcard in user_permissions:
                return True
        
        return False
    
    def check_permissions(
        self,
        user_permissions: List[str],
        required_permissions: List[str],
        require_all: bool = False
    ) -> bool:
        """
        Check if user has required permissions.
        
        Args:
            user_permissions: List of user permissions
            required_permissions: List of required permissions
            require_all: If True, user must have all permissions.
                        If False, user needs only one.
        """
        if require_all:
            return all(
                self.check_permission(user_permissions, perm)
                for perm in required_permissions
            )
        else:
            return any(
                self.check_permission(user_permissions, perm)
                for perm in required_permissions
            )
    
    def get_missing_permissions(
        self,
        user_permissions: List[str],
        required_permissions: List[str]
    ) -> List[str]:
        """Get list of permissions user doesn't have."""
        missing = []
        for perm in required_permissions:
            if not self.check_permission(user_permissions, perm):
                missing.append(perm)
        return missing
    
    def expand_wildcard_permissions(
        self,
        permissions: List[str],
        available_permissions: List[str]
    ) -> Set[str]:
        """
        Expand wildcard permissions to all matching permissions.
        
        Example: "users.*" expands to ["users.read", "users.write", "users.delete"]
        """
        expanded = set()
        
        for perm in permissions:
            if perm == "*":
                return set(available_permissions)
            
            if "*" in perm:
                # It's a wildcard pattern
                resource = perm.replace(".*", "").replace("*", "")
                for avail in available_permissions:
                    if avail.startswith(f"{resource}."):
                        expanded.add(avail)
            else:
                expanded.add(perm)
        
        return expanded
    
    def validate_permission_format(self, permission: str) -> bool:
        """Validate permission string format (resource.action)."""
        if not permission:
            return False
        
        if permission == "*":
            return True
        
        parts = permission.split(".")
        if len(parts) != 2:
            return False
        
        resource, action = parts
        
        if not resource or not action:
            return False
        
        return True
    
    def get_permission_hierarchy(
        self,
        role_level: int,
        target_role_level: int
    ) -> str:
        """Get relationship between two roles based on levels."""
        if role_level > target_role_level:
            return "higher"
        elif role_level == target_role_level:
            return "same"
        else:
            return "lower"
    
    def can_modify_role(
        self,
        modifier_level: int,
        target_role_level: int,
        is_target_system: bool
    ) -> bool:
        """Check if user can modify a role."""
        # System roles can only be modified by superusers
        if is_target_system and modifier_level < 100:
            return False
        
        # Can only modify roles at same or lower level
        return modifier_level >= target_role_level

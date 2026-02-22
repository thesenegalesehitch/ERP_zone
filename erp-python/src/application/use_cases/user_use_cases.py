"""
Application Layer - User Use Cases
Business logic orchestration for user operations.

Author: Alexandre Albert Ndour
"""

from typing import Optional, List
import uuid

from ..dtos.user_dtos import (
    CreateUserDTO,
    UpdateUserDTO,
    UserResponseDTO,
    UserListDTO,
    LoginDTO,
    LoginResponseDTO,
    ChangePasswordDTO,
    AssignRoleDTO,
    PaginationParams,
    UserFilterDTO,
)
from ...domain.entities.user import User
from ...domain.entities.role import Role
from ...domain.value_objects.email import Email
from ...domain.events.user_events import (
    UserCreatedEvent,
    UserUpdatedEvent,
    UserDeletedEvent,
    UserActivatedEvent,
    UserDeactivatedEvent,
    PasswordChangedEvent,
)


class CreateUserUseCase:
    """Use case for creating a new user."""
    
    def __init__(
        self,
        user_repository,
        role_repository,
        password_hasher,
        event_dispatcher
    ):
        self.user_repository = user_repository
        self.role_repository = role_repository
        self.password_hasher = password_hasher
        self.event_dispatcher = event_dispatcher
    
    async def execute(
        self,
        dto: CreateUserDTO,
        created_by: uuid.UUID = None
    ) -> UserResponseDTO:
        # Check if email already exists
        if await self.user_repository.exists(dto.email):
            raise ValueError("Email already registered")
        
        # Validate password strength
        from ...domain.value_objects.password import Password
        errors = Password.validate_strength(dto.password)
        if errors:
            raise ValueError(f"Invalid password: {', '.join(errors)}")
        
        # Hash password
        password_hash = await self.password_hasher.hash(dto.password)
        
        # Create user entity
        user = User.create(
            email=dto.email,
            password_hash=password_hash,
            first_name=dto.first_name,
            last_name=dto.last_name,
            phone=dto.phone,
            created_by=created_by
        )
        
        # Save user
        created_user = await self.user_repository.create(user)
        
        # Assign roles if provided
        for role_id in dto.role_ids:
            role = await self.role_repository.get_by_id(role_id)
            if role:
                created_user.add_role(role_id)
        
        await self.user_repository.update(created_user)
        
        # Dispatch event
        event = UserCreatedEvent(
            user_id=created_user.id,
            email=str(created_user.email),
            first_name=created_user.first_name,
            last_name=created_user.last_name,
            created_by=created_by
        )
        await self.event_dispatcher.dispatch(event)
        
        return UserResponseDTO(
            id=created_user.id,
            email=str(created_user.email),
            first_name=created_user.first_name,
            last_name=created_user.last_name,
            phone=created_user.phone,
            avatar_url=created_user.avatar_url,
            is_active=created_user.is_active,
            is_verified=created_user.is_verified,
            is_superuser=created_user.is_superuser,
            last_login_at=created_user.last_login_at,
            created_at=created_user.created_at,
            updated_at=created_user.updated_at,
            roles=[str(r) for r in created_user.roles],
            permissions=created_user.permissions
        )


class LoginUseCase:
    """Use case for user authentication."""
    
    def __init__(
        self,
        user_repository,
        password_hasher,
        token_generator,
        domain_service
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.token_generator = token_generator
        self.domain_service = domain_service
    
    async def execute(self, dto: LoginDTO) -> LoginResponseDTO:
        # Get user by email
        user = await self.user_repository.get_by_email(dto.email)
        if not user:
            raise ValueError("Invalid credentials")
        
        # Check if user can login
        can_login, reason = self.domain_service.validate_user_status_for_login(
            user.is_active,
            user.is_locked,
            user.is_verified
        )
        if not can_login:
            raise ValueError(reason)
        
        # Verify password
        if not await self.password_hasher.verify(dto.password, user.password_hash):
            user.record_failed_login()
            await self.user_repository.update(user)
            raise ValueError("Invalid credentials")
        
        # Record successful login
        user.record_successful_login()
        await self.user_repository.update(user)
        
        # Generate tokens
        access_token = await self.token_generator.generate_access_token(user)
        refresh_token = await self.token_generator.generate_refresh_token(user)
        
        return LoginResponseDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserResponseDTO(
                id=user.id,
                email=str(user.email),
                first_name=user.first_name,
                last_name=user.last_name,
                phone=user.phone,
                avatar_url=user.avatar_url,
                is_active=user.is_active,
                is_verified=user.is_verified,
                is_superuser=user.is_superuser,
                last_login_at=user.last_login_at,
                created_at=user.created_at,
                updated_at=user.updated_at,
                roles=[str(r) for r in user.roles],
                permissions=user.permissions
            )
        )


class UpdateUserUseCase:
    """Use case for updating user information."""
    
    def __init__(self, user_repository, event_dispatcher):
        self.user_repository = user_repository
        self.event_dispatcher = event_dispatcher
    
    async def execute(
        self,
        user_id: uuid.UUID,
        dto: UpdateUserDTO,
        updated_by: uuid.UUID = None
    ) -> UserResponseDTO:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Track changes
        updated_fields = []
        
        if dto.first_name is not None and dto.first_name != user.first_name:
            user.first_name = dto.first_name
            updated_fields.append("first_name")
        
        if dto.last_name is not None and dto.last_name != user.last_name:
            user.last_name = dto.last_name
            updated_fields.append("last_name")
        
        if dto.phone is not None and dto.phone != user.phone:
            user.phone = dto.phone
            updated_fields.append("phone")
        
        if dto.avatar_url is not None:
            user.avatar_url = dto.avatar_url
            updated_fields.append("avatar_url")
        
        if dto.is_active is not None and dto.is_active != user.is_active:
            user.is_active = dto.is_active
            updated_fields.append("is_active")
        
        # Save changes
        updated_user = await self.user_repository.update(user)
        
        # Dispatch event
        if updated_fields:
            event = UserUpdatedEvent(
                user_id=user.id,
                updated_fields=updated_fields,
                updated_by=updated_by
            )
            await self.event_dispatcher.dispatch(event)
        
        return UserResponseDTO(
            id=updated_user.id,
            email=str(updated_user.email),
            first_name=updated_user.first_name,
            last_name=updated_user.last_name,
            phone=updated_user.phone,
            avatar_url=updated_user.avatar_url,
            is_active=updated_user.is_active,
            is_verified=updated_user.is_verified,
            is_superuser=updated_user.is_superuser,
            last_login_at=updated_user.last_login_at,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at,
            roles=[str(r) for r in updated_user.roles],
            permissions=updated_user.permissions
        )


class GetUserUseCase:
    """Use case for retrieving a user."""
    
    def __init__(self, user_repository, role_repository):
        self.user_repository = user_repository
        self.role_repository = role_repository
    
    async def execute(self, user_id: uuid.UUID) -> UserResponseDTO:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        return UserResponseDTO(
            id=user.id,
            email=str(user.email),
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone,
            avatar_url=user.avatar_url,
            is_active=user.is_active,
            is_verified=user.is_verified,
            is_superuser=user.is_superuser,
            last_login_at=user.last_login_at,
            created_at=user.created_at,
            updated_at=user.updated_at,
            roles=[str(r) for r in user.roles],
            permissions=user.permissions
        )


class ListUsersUseCase:
    """Use case for listing users."""
    
    def __init__(self, user_repository):
        self.user_repository = user_repository
    
    async def execute(
        self,
        filters: UserFilterDTO = None,
        pagination: PaginationParams = None
    ) -> tuple[List[UserListDTO], int]:
        if filters is None:
            filters = UserFilterDTO()
        if pagination is None:
            pagination = PaginationParams()
        
        filter_dict = {}
        if filters.is_active is not None:
            filter_dict["is_active"] = filters.is_active
        if filters.is_verified is not None:
            filter_dict["is_verified"] = filters.is_verified
        if filters.search:
            filter_dict["search"] = filters.search
        
        users, total = await self.user_repository.list(
            filters=filter_dict,
            page=pagination.page,
            limit=pagination.limit
        )
        
        user_list = [
            UserListDTO(
                id=user.id,
                email=str(user.email),
                first_name=user.first_name,
                last_name=user.last_name,
                is_active=user.is_active,
                is_verified=user.is_verified,
                created_at=user.created_at
            )
            for user in users
        ]
        
        return user_list, total


class DeleteUserUseCase:
    """Use case for deleting a user."""
    
    def __init__(self, user_repository, event_dispatcher):
        self.user_repository = user_repository
        self.event_dispatcher = event_dispatcher
    
    async def execute(
        self,
        user_id: uuid.UUID,
        deleted_by: uuid.UUID = None
    ) -> bool:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Prevent deleting superuser
        if user.is_superuser:
            raise ValueError("Cannot delete superuser account")
        
        result = await self.user_repository.delete(user_id)
        
        # Dispatch event
        if result:
            event = UserDeletedEvent(
                user_id=user.id,
                deleted_by=deleted_by
            )
            await self.event_dispatcher.dispatch(event)
        
        return result


class AssignRoleUseCase:
    """Use case for assigning a role to a user."""
    
    def __init__(self, user_repository, role_repository, user_role_repository):
        self.user_repository = user_repository
        self.role_repository = role_repository
        self.user_role_repository = user_role_repository
    
    async def execute(
        self,
        user_id: uuid.UUID,
        dto: AssignRoleDTO,
        assigned_by: uuid.UUID = None
    ) -> UserResponseDTO:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        role = await self.role_repository.get_by_id(dto.role_id)
        if not role:
            raise ValueError("Role not found")
        
        if not role.is_active:
            raise ValueError("Cannot assign inactive role")
        
        # Check if already assigned
        if await self.user_role_repository.has_role(user_id, dto.role_id):
            raise ValueError("User already has this role")
        
        # Assign role
        await self.user_role_repository.assign_role(
            user_id=user_id,
            role_id=dto.role_id,
            assigned_by=assigned_by
        )
        
        # Refresh user
        user = await self.user_repository.get_by_id(user_id)
        
        return UserResponseDTO(
            id=user.id,
            email=str(user.email),
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone,
            avatar_url=user.avatar_url,
            is_active=user.is_active,
            is_verified=user.is_verified,
            is_superuser=user.is_superuser,
            last_login_at=user.last_login_at,
            created_at=user.created_at,
            updated_at=user.updated_at,
            roles=[str(r) for r in user.roles],
            permissions=user.permissions
        )

"""
Infrastructure Layer - Password Hasher
Secure password hashing implementation.

Author: Alexandre Albert Ndour
"""

from abc import ABC, abstractmethod
import hashlib
import hmac
import secrets
import math


class PasswordHasherInterface(ABC):
    """Interface for password hashing."""
    
    @abstractmethod
    async def hash(self, password: str) -> str:
        """Hash a password."""
        pass
    
    @abstractmethod
    async def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against a hash."""
        pass


class BcryptHasher(PasswordHasherInterface):
    """Bcrypt password hasher."""
    
    def __init__(self, rounds: int = 12):
        self.rounds = rounds
    
    async def hash(self, password: str) -> str:
        """Hash a password using bcrypt."""
        import bcrypt
        salt = bcrypt.gensalt(rounds=self.rounds)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    async def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against a bcrypt hash."""
        import bcrypt
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )


class Argon2Hasher(PasswordHasherInterface):
    """Argon2 password hasher (recommended)."""
    
    def __init__(
        self,
        time_cost: int = 2,
        memory_cost: int = 65536,
        parallelism: int = 1
    ):
        self.time_cost = time_cost
        self.memory_cost = memory_cost
        self.parallelism = parallelism
    
    async def hash(self, password: str) -> str:
        """Hash a password using argon2."""
        import argon2
        hasher = argon2.PasswordHasher(
            time_cost=self.time_cost,
            memory_cost=self.memory_cost,
            parallelism=self.parallelism
        )
        return hasher.hash(password)
    
    async def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against an argon2 hash."""
        import argon2
        hasher = argon2.PasswordHasher()
        try:
            hasher.verify(hashed_password, plain_password)
            return True
        except argon2.exceptions.VerifyMismatchError:
            return False
        except Exception:
            return False


class PBKDF2Hasher(PasswordHasherInterface):
    """PBKDF2 password hasher."""
    
    def __init__(self, iterations: int = 100000, key_length: int = 32):
        self.iterations = iterations
        self.key_length = key_length
        self.salt_length = 16
    
    async def hash(self, password: str) -> str:
        """Hash a password using PBKDF2."""
        salt = secrets.token_hex(self.salt_length)
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            self.iterations,
            dklen=self.key_length
        )
        return f"{salt}${key.hex()}"
    
    async def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against a PBKDF2 hash."""
        try:
            parts = hashed_password.split('$')
            if len(parts) != 2:
                return False
            
            salt, stored_key = parts
            key = hashlib.pbkdf2_hmac(
                'sha256',
                plain_password.encode('utf-8'),
                salt.encode('utf-8'),
                self.iterations,
                dklen=self.key_length
            )
            return hmac.compare_digest(key.hex(), stored_key)
        except Exception:
            return False


# Default hasher (using bcrypt for compatibility)
DefaultPasswordHasher = BcryptHasher

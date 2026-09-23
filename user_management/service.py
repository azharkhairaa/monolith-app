"""Lapisan use case (aplikasi)."""

from __future__ import annotations

from typing import List

from user_management import domain
from user_management.domain import User
from user_management.ports import UserRepository


class UserService:
    """Service untuk use case user."""

    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def create_user(self, name: str, email: str) -> User:
        """Mendaftarkan user baru dan menyimpannya."""
        existing = self._repository.list_all()
        user = domain.register(existing, name, email)
        self._repository.add(user)
        return user

    def list_users(self) -> List[User]:
        """Mengembalikan seluruh user yang tersimpan."""
        return self._repository.list_all()

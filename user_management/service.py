"""Use case (lapisan aplikasi): merangkai aturan domain dengan penyimpanan.

Modul ini tahu *urutan langkah* sebuah use case, tapi tidak tahu aturan
bisnisnya (ada di ``domain``) maupun cara menyimpannya (ada di ``storage``).
"""

from __future__ import annotations

from typing import List

from user_management import domain
from user_management.domain import User
from user_management.ports import UserRepository


class UserService:
    """Pintu masuk seluruh use case user.

    Penyimpanan disuntikkan lewat konstruktor (*dependency injection*), jadi
    kelas ini tidak pernah menentukan sendiri ke mana data ditulis.
    """

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

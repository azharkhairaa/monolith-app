"""Kontrak penyimpanan user."""

from __future__ import annotations

from typing import List, Protocol, runtime_checkable

from user_management.domain import User


@runtime_checkable
class UserRepository(Protocol):
    """Interface penyimpanan user."""

    def list_all(self) -> List[User]:
        """Mengembalikan seluruh user yang tersimpan, urut penyimpanan."""
        ...

    def add(self, user: User) -> None:
        """Menyimpan satu user baru."""
        ...

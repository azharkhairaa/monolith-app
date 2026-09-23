"""Adapter penyimpanan di memori.

Dipakai oleh test (dan berguna untuk mencoba aplikasi tanpa menyentuh berkas).
Keberadaannya adalah bukti bahwa ``service`` benar-benar lepas dari berkas:
kalau masih terikat, adapter ini tidak akan bisa menggantikannya.
"""

from __future__ import annotations

from typing import Iterable, List, Optional

from user_management.domain import User


class InMemoryUserRepository:
    """Menyimpan user pada list biasa selama proses hidup."""

    def __init__(self, users: Optional[Iterable[User]] = None) -> None:
        self._users: List[User] = list(users) if users else []

    def list_all(self) -> List[User]:
        # Salinan, supaya pemanggil tidak bisa mengubah isi penyimpanan
        # lewat list yang dikembalikan.
        return list(self._users)

    def add(self, user: User) -> None:
        self._users.append(user)

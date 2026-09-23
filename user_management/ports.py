"""Kontrak (port) yang harus dipenuhi setiap penyimpanan user.

Hanya deklarasi, tanpa implementasi. Modul ini yang membalik arah
ketergantungan: ``service`` bicara ke kontrak ini, bukan ke adapter berkas.
"""

from __future__ import annotations

from typing import List, Protocol, runtime_checkable

from user_management.domain import User


@runtime_checkable
class UserRepository(Protocol):
    """Penyimpanan user.

    Sengaja dibuat sekecil mungkin: dua operasi yang benar-benar dipakai
    use case. Makin kecil port-nya, makin murah menulis adapter baru
    (SQLite, API, in-memory untuk uji).
    """

    def list_all(self) -> List[User]:
        """Mengembalikan seluruh user yang tersimpan, urut penyimpanan."""
        ...

    def add(self, user: User) -> None:
        """Menyimpan satu user baru."""
        ...

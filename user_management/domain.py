"""Aturan bisnis user — lapisan paling dalam.

Modul ini murni: tidak mengimpor modul lain dari paket ini, tidak membuka
berkas, tidak membaca input, tidak mencetak apa pun. Semua fungsi di sini bisa
diuji tanpa menyiapkan berkas atau mem-patch apa pun.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Iterable, List, Optional


class UserError(ValueError):
    """Induk semua pelanggaran aturan bisnis user.

    Sengaja diturunkan dari ``ValueError`` supaya pemanggil lama yang menulis
    ``except ValueError`` tetap bekerja setelah refactor.
    """


class ValidationError(UserError):
    """Data masukan tidak memenuhi aturan penulisan."""


class DuplicateEmailError(UserError):
    """Email sudah dipakai user lain."""


@dataclass(frozen=True)
class User:
    """Entitas user.

    ``id`` bernilai ``None`` selama user belum terdaftar; nilainya diisi oleh
    :func:`register`. Bentuk penyimpanannya (dict JSON, baris tabel, dokumen)
    bukan urusan modul ini.
    """

    name: str
    email: str
    id: Optional[int] = None


def validate_user(name: str, email: str) -> User:
    """Membersihkan dan memvalidasi masukan mentah menjadi satu ``User``."""
    if not name or not name.strip():
        raise ValidationError("Name cannot be empty")

    if "@" not in email:
        raise ValidationError("Invalid email")

    return User(name=name.strip(), email=email.strip().lower())


def is_email_taken(users: Iterable[User], email: str) -> bool:
    """Apakah ``email`` sudah dipakai salah satu user pada koleksi."""
    return any(existing.email == email for existing in users)


def next_user_id(users: Iterable[User]) -> int:
    """Nomor id untuk user berikutnya.

    Sengaja mempertahankan perilaku kode awal (``len(users) + 1``) supaya
    refactor ini tidak mengubah hasil. Rumus ini rapuh kalau nanti ada fitur
    hapus user — id bisa bentrok. Dicatat sebagai temuan di README, bukan
    diperbaiki diam-diam di tugas ini.
    """
    return len(list(users)) + 1


def register(existing_users: Iterable[User], name: str, email: str) -> User:
    """Aturan pendaftaran user baru, dalam satu tempat.

    Menerima koleksi user yang sudah ada sebagai *nilai* — dari mana koleksi
    itu datang (berkas, memori, database) bukan urusan lapisan ini.
    """
    candidate = validate_user(name, email)
    existing: List[User] = list(existing_users)

    if is_email_taken(existing, candidate.email):
        raise DuplicateEmailError("Email already exists")

    return replace(candidate, id=next_user_id(existing))

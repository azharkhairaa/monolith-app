"""Aturan bisnis user."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Iterable, List, Optional


class UserError(ValueError):
    """Induk pelanggaran aturan bisnis user."""


class ValidationError(UserError):
    """Data masukan tidak memenuhi aturan penulisan."""


class DuplicateEmailError(UserError):
    """Email sudah dipakai user lain."""


@dataclass(frozen=True)
class User:
    """Entitas user."""

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
    """Nomor id untuk user berikutnya."""
    return len(list(users)) + 1


def register(existing_users: Iterable[User], name: str, email: str) -> User:
    """Pendaftaran user baru."""
    candidate = validate_user(name, email)
    existing: List[User] = list(existing_users)

    if is_email_taken(existing, candidate.email):
        raise DuplicateEmailError("Email already exists")

    return replace(candidate, id=next_user_id(existing))

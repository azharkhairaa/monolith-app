"""Antarmuka CLI."""

from __future__ import annotations

from typing import Callable

from user_management.domain import User, UserError
from user_management.service import UserService

EXIT_OK = 0
EXIT_INVALID_INPUT = 1


def format_user(user: User) -> str:
    """Bentuk tampilan satu user di terminal."""
    return f"#{user.id} {user.name} <{user.email}>"


def run(
    service: UserService,
    read_line: Callable[[str], str] = input,
    write_line: Callable[[str], None] = print,
) -> int:
    """Alur pendaftaran user."""
    name = read_line("Name: ")
    email = read_line("Email: ")

    try:
        user = service.create_user(name, email)
    except UserError as error:
        write_line(f"Error: {error}")
        return EXIT_INVALID_INPUT

    write_line(f"User created: {format_user(user)}")
    return EXIT_OK

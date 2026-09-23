"""Titik masuk aplikasi (composition root)."""

from __future__ import annotations

import sys
from pathlib import Path

from user_management.cli import run
from user_management.service import UserService
from user_management.storage.json_file import JsonFileUserRepository

# Path data relatif terhadap berkas ini.
DATA_FILE = Path(__file__).resolve().parent / "users.json"


def main() -> int:
    repository = JsonFileUserRepository(DATA_FILE)
    service = UserService(repository)
    return run(service)


if __name__ == "__main__":
    sys.exit(main())

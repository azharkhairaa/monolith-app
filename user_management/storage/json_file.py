"""Adapter penyimpanan berkas JSON.

Satu-satunya modul yang tahu bahwa data disimpan sebagai berkas JSON dan tahu
nama-nama kuncinya. Kalau format penyimpanan berganti, hanya berkas ini yang
ditulis ulang.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Union

from user_management.domain import User


class JsonFileUserRepository:
    """Menyimpan user pada satu berkas JSON berisi array objek."""

    def __init__(self, path: Union[str, Path]) -> None:
        self._path = Path(path)

    def list_all(self) -> List[User]:
        return [_to_user(row) for row in self._read_rows()]

    def add(self, user: User) -> None:
        rows = self._read_rows()
        rows.append(_to_row(user))
        self._write_rows(rows)

    def _read_rows(self) -> List[Dict[str, Any]]:
        if not self._path.exists():
            return []

        with self._path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _write_rows(self, rows: List[Dict[str, Any]]) -> None:
        with self._path.open("w", encoding="utf-8") as file:
            json.dump(rows, file, indent=2)


def _to_user(row: Dict[str, Any]) -> User:
    """JSON -> domain. Pemetaan ini sengaja hanya ada di adapter."""
    return User(name=row["name"], email=row["email"], id=row.get("id"))


def _to_row(user: User) -> Dict[str, Any]:
    """Domain -> JSON, dengan urutan kunci mengikuti isi ``users.json``."""
    return {"id": user.id, "name": user.name, "email": user.email}

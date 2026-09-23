"""Uji antarmuka CLI."""

from user_management.cli import EXIT_INVALID_INPUT, EXIT_OK, run
from user_management.domain import User
from user_management.service import UserService
from user_management.storage.memory import InMemoryUserRepository


class TerminalPalsu:
    """Mock untuk input() dan print()."""

    def __init__(self, jawaban):
        self._jawaban = list(jawaban)
        self.prompt = []
        self.keluaran = []

    def read_line(self, prompt):
        self.prompt.append(prompt)
        return self._jawaban.pop(0)

    def write_line(self, teks):
        self.keluaran.append(teks)


def test_alur_sukses_mencetak_user_dan_menyimpannya():
    repository = InMemoryUserRepository()
    terminal = TerminalPalsu([" Alice ", "ALICE@example.com"])

    kode = run(UserService(repository), terminal.read_line, terminal.write_line)

    assert kode == EXIT_OK
    assert terminal.prompt == ["Name: ", "Email: "]
    assert terminal.keluaran == ["User created: #1 Alice <alice@example.com>"]
    assert repository.list_all() == [User(name="Alice", email="alice@example.com", id=1)]


def test_email_tidak_valid_dilaporkan_sebagai_error():
    terminal = TerminalPalsu(["Alice", "invalid-email"])

    kode = run(UserService(InMemoryUserRepository()), terminal.read_line, terminal.write_line)

    assert kode == EXIT_INVALID_INPUT
    assert terminal.keluaran == ["Error: Invalid email"]


def test_email_duplikat_dilaporkan_sebagai_error():
    repository = InMemoryUserRepository([User(name="Alice", email="alice@example.com", id=1)])
    terminal = TerminalPalsu(["Alice Lain", "alice@example.com"])

    kode = run(UserService(repository), terminal.read_line, terminal.write_line)

    assert kode == EXIT_INVALID_INPUT
    assert terminal.keluaran == ["Error: Email already exists"]
    assert len(repository.list_all()) == 1

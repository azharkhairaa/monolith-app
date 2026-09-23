"""Uji use case dengan penyimpanan memori."""

import pytest

from user_management.domain import DuplicateEmailError, User, ValidationError
from user_management.service import UserService
from user_management.storage.memory import InMemoryUserRepository


@pytest.fixture
def repository():
    return InMemoryUserRepository()


@pytest.fixture
def service(repository):
    return UserService(repository)


def test_create_user_menyimpan_user_yang_sudah_dirapikan(service, repository):
    user = service.create_user(" Alice ", "ALICE@example.com")

    assert user == User(name="Alice", email="alice@example.com", id=1)
    assert repository.list_all() == [user]


def test_id_bertambah_untuk_user_berikutnya(service):
    service.create_user("Alice", "alice@example.com")
    kedua = service.create_user("Budi", "budi@example.com")

    assert kedua.id == 2


def test_email_duplikat_ditolak_dan_tidak_ikut_tersimpan(service, repository):
    service.create_user("Alice", "alice@example.com")

    with pytest.raises(DuplicateEmailError):
        service.create_user("Alice Lain", "alice@example.com")

    assert len(repository.list_all()) == 1


def test_masukan_tidak_valid_tidak_menyentuh_penyimpanan(repository):
    class RepositoryYangMenolakTulis:
        """Mock repository yang menolak tulis."""

        def __init__(self):
            self.pemanggilan = []

        def list_all(self):
            self.pemanggilan.append("list_all")
            return []

        def add(self, user):
            raise AssertionError("add() tidak boleh dipanggil untuk masukan tidak valid")

    penyimpanan = RepositoryYangMenolakTulis()

    with pytest.raises(ValidationError):
        UserService(penyimpanan).create_user("", "alice@example.com")

    assert penyimpanan.pemanggilan == ["list_all"]


def test_list_users_mengembalikan_isi_penyimpanan():
    tersimpan = [
        User(name="Alice", email="alice@example.com", id=1),
        User(name="Budi", email="budi@example.com", id=2),
    ]

    assert UserService(InMemoryUserRepository(tersimpan)).list_users() == tersimpan

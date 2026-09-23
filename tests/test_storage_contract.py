"""Uji kontrak semua adapter penyimpanan."""

import pytest

from user_management.domain import User
from user_management.ports import UserRepository
from user_management.service import UserService
from user_management.storage.json_file import JsonFileUserRepository
from user_management.storage.memory import InMemoryUserRepository


@pytest.fixture(params=["memory", "json_file"])
def repository(request, tmp_path):
    if request.param == "memory":
        return InMemoryUserRepository()
    return JsonFileUserRepository(tmp_path / "users.json")


def test_adapter_memenuhi_port(repository):
    assert isinstance(repository, UserRepository)


def test_penyimpanan_baru_masih_kosong(repository):
    assert repository.list_all() == []


def test_user_yang_ditambahkan_bisa_dibaca_lagi(repository):
    user = User(name="Alice", email="alice@example.com", id=1)

    repository.add(user)

    assert repository.list_all() == [user]


def test_urutan_penambahan_dipertahankan(repository):
    pertama = User(name="Alice", email="alice@example.com", id=1)
    kedua = User(name="Budi", email="budi@example.com", id=2)

    repository.add(pertama)
    repository.add(kedua)

    assert repository.list_all() == [pertama, kedua]


def test_service_bekerja_di_atas_adapter_mana_pun(repository):
    service = UserService(repository)

    service.create_user("Alice", "alice@example.com")
    service.create_user("Budi", "budi@example.com")

    assert [user.email for user in service.list_users()] == [
        "alice@example.com",
        "budi@example.com",
    ]

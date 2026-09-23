"""Uji aturan bisnis murni — tanpa berkas, tanpa mock, tanpa tmp_path."""

import pytest

from user_management.domain import (
    DuplicateEmailError,
    User,
    ValidationError,
    is_email_taken,
    next_user_id,
    register,
    validate_user,
)


def test_validate_user_merapikan_spasi_dan_huruf_besar():
    # Turunan langsung dari test_validate_user() pada kode awal.
    user = validate_user(" Alice ", "ALICE@example.com")

    assert user == User(name="Alice", email="alice@example.com", id=None)


def test_email_tanpa_at_ditolak():
    # Turunan langsung dari test_invalid_email() pada kode awal.
    with pytest.raises(ValidationError) as error:
        validate_user("Alice", "invalid-email")

    assert str(error.value) == "Invalid email"


@pytest.mark.parametrize("nama_kosong", ["", "   ", "\t"])
def test_nama_kosong_ditolak(nama_kosong):
    with pytest.raises(ValidationError) as error:
        validate_user(nama_kosong, "alice@example.com")

    assert str(error.value) == "Name cannot be empty"


def test_error_domain_tetap_bisa_ditangkap_sebagai_value_error():
    # Jaring pengaman kompatibilitas: pemanggil lama menulis `except ValueError`.
    with pytest.raises(ValueError):
        validate_user("", "alice@example.com")


def test_is_email_taken_membandingkan_email_yang_sudah_dinormalkan():
    users = [User(name="Alice", email="alice@example.com", id=1)]

    assert is_email_taken(users, "alice@example.com") is True
    assert is_email_taken(users, "budi@example.com") is False


def test_next_user_id_melanjutkan_jumlah_user():
    assert next_user_id([]) == 1
    assert next_user_id([User("Alice", "a@x.id", 1), User("Budi", "b@x.id", 2)]) == 3


def test_register_memberi_id_dan_merapikan_data():
    existing = [User(name="Alice", email="alice@example.com", id=1)]

    user = register(existing, " Budi ", "BUDI@example.com")

    assert user == User(name="Budi", email="budi@example.com", id=2)


def test_register_menolak_email_duplikat_meski_beda_huruf_besar():
    existing = [User(name="Alice", email="alice@example.com", id=1)]

    with pytest.raises(DuplicateEmailError) as error:
        register(existing, "Alice Lain", "ALICE@example.com")

    assert str(error.value) == "Email already exists"


def test_register_tidak_mengubah_koleksi_yang_diterima():
    existing = [User(name="Alice", email="alice@example.com", id=1)]

    register(existing, "Budi", "budi@example.com")

    assert existing == [User(name="Alice", email="alice@example.com", id=1)]

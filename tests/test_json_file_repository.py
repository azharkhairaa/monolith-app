"""Uji adapter berkas JSON."""

import json

from user_management.domain import User
from user_management.storage.json_file import JsonFileUserRepository


def test_berkas_belum_ada_dianggap_kosong(tmp_path):
    repository = JsonFileUserRepository(tmp_path / "belum-ada.json")

    assert repository.list_all() == []


def test_add_tidak_membuat_berkas_sebelum_ada_data(tmp_path):
    path = tmp_path / "users.json"
    JsonFileUserRepository(path).list_all()

    assert not path.exists()


def test_membaca_berkas_yang_sudah_ada(tmp_path):
    path = tmp_path / "users.json"
    path.write_text(
        json.dumps([{"id": 1, "name": "Alice", "email": "alice@example.com"}]),
        encoding="utf-8",
    )

    assert JsonFileUserRepository(path).list_all() == [
        User(name="Alice", email="alice@example.com", id=1)
    ]


def test_bentuk_berkas_hasil_tulis_sesuai_format_users_json(tmp_path):
    path = tmp_path / "users.json"
    repository = JsonFileUserRepository(path)

    repository.add(User(name="Alice", email="alice@example.com", id=1))

    assert json.loads(path.read_text(encoding="utf-8")) == [
        {"id": 1, "name": "Alice", "email": "alice@example.com"}
    ]
    # Pastikan format indent=2.
    assert path.read_text(encoding="utf-8").startswith('[\n  {\n    "id": 1')


def test_add_tidak_menimpa_isi_lama(tmp_path):
    path = tmp_path / "users.json"
    repository = JsonFileUserRepository(path)

    repository.add(User(name="Alice", email="alice@example.com", id=1))
    repository.add(User(name="Budi", email="budi@example.com", id=2))

    assert len(json.loads(path.read_text(encoding="utf-8"))) == 2


def test_nama_non_ascii_terbaca_utuh(tmp_path):
    path = tmp_path / "users.json"
    repository = JsonFileUserRepository(path)

    repository.add(User(name="Citra Ayu Utamiñ", email="citra@example.com", id=1))

    assert repository.list_all()[0].name == "Citra Ayu Utamiñ"

"""Menjaga arah panah dependensi antar-module.

Aturan pembagian module gampang rusak diam-diam: satu ``import`` yang
kelihatannya praktis sudah cukup membuat domain kembali terikat ke berkas.
Test ini membaca ``import`` tiap module dengan ``ast`` dan menolak panah yang
arahnya keluar.
"""

import ast
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PAKET = "user_management"

# Module -> daftar module internal yang boleh diimpor.
IZIN = {
    "user_management.domain": set(),
    "user_management.ports": {"user_management.domain"},
    "user_management.service": {"user_management.domain", "user_management.ports"},
    "user_management.cli": {
        "user_management.domain",
        "user_management.ports",
        "user_management.service",
    },
    "user_management.storage.json_file": {"user_management.domain", "user_management.ports"},
    "user_management.storage.memory": {"user_management.domain", "user_management.ports"},
}


def _nama_module(path: Path) -> str:
    return ".".join(path.relative_to(ROOT).with_suffix("").parts)


def _import_internal(path: Path) -> set:
    """Nama module internal yang diimpor berkas ini (diabaikan: pustaka standar)."""
    pohon = ast.parse(path.read_text(encoding="utf-8"))
    hasil = set()

    for simpul in ast.walk(pohon):
        if isinstance(simpul, ast.Import):
            hasil.update(alias.name for alias in simpul.names)
        elif isinstance(simpul, ast.ImportFrom) and simpul.module:
            hasil.add(simpul.module)
            hasil.update(f"{simpul.module}.{alias.name}" for alias in simpul.names)

    # `from user_management import domain` membuat AST mencatat paket induknya
    # juga; paket induk sendiri tidak membawa dependensi apa pun (__init__.py
    # kosong dari import), jadi yang dinilai hanya module di dalamnya.
    return {nama for nama in hasil if nama.startswith(PAKET + ".")}


MODULE = sorted(
    path
    for path in (ROOT / PAKET).rglob("*.py")
    if path.name != "__init__.py"
)


@pytest.mark.parametrize("path", MODULE, ids=_nama_module)
def test_module_hanya_mengimpor_yang_diizinkan(path):
    nama = _nama_module(path)
    diizinkan = IZIN[nama] | {nama}
    dilanggar = {
        impor
        for impor in _import_internal(path)
        if not any(impor == boleh or impor.startswith(boleh + ".") for boleh in diizinkan)
    }

    assert not dilanggar, f"{nama} tidak boleh mengimpor {sorted(dilanggar)}"


def test_domain_tidak_bergantung_pada_apa_pun_di_dalam_paket():
    assert _import_internal(ROOT / PAKET / "domain.py") == set()


def test_hanya_main_yang_memilih_adapter_konkret():
    pemakai_storage = {
        _nama_module(path)
        for path in [*MODULE, ROOT / "main.py"]
        if any(impor.startswith(f"{PAKET}.storage") for impor in _import_internal(path))
    }

    assert pemakai_storage == {"main"}


def test_seluruh_module_terdaftar_pada_aturan():
    # Supaya module baru tidak lolos tanpa aturan arah dependensi.
    assert {_nama_module(path) for path in MODULE} == set(IZIN)

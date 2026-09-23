"""Adapter penyimpanan — implementasi konkret dari ``user_management.ports``.

Isi paket ini boleh mengimpor ``domain`` dan ``ports``, tetapi tidak boleh
diimpor oleh ``domain``, ``ports``, ``service``, maupun ``cli``. Yang memilih
adapter mana yang dipakai hanyalah ``main.py``.
"""

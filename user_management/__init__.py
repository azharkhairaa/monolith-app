"""Paket manajemen user.

Lapisan (dari dalam ke luar):

    domain  <-  ports  <-  service  <-  cli
                  ^
                  |
              storage/*   (adapter, mengimplementasikan port)

Aturan yang dijaga: panah impor selalu mengarah ke dalam. ``domain`` tidak
mengimpor apa pun dari paket ini, dan tidak ada modul di dalam paket yang
mengimpor ``storage`` — pemilihan adapter hanya terjadi di ``main.py``.
"""

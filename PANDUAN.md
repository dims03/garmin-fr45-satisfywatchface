# SATISFY untuk Garmin Forerunner 45

Watch face dengan jam besar dan tulisan SATISFY, berdasarkan gambar referensi Anda.
Target: **Forerunner 45 / fr45, 208 x 208, Connect IQ 1.4.x**.

## Isi tampilan

- Waktu mengikuti pengaturan 12/24 jam pada perangkat.
- Hari (bahasa Inggris) dan tanggal DD.MM.
- Baterai: ikon dan persentase dari perangkat.
- DIST: jarak harian sejak tengah malam, dalam kilometer. Ini bukan jarak sesi lari.
- STEPS: jumlah langkah hari ini.
- HEART RATE: sampel detak jantung terakhir dari riwayat jam. `-- BPM` jika tidak ada sampel valid dalam 10 menit terakhir. Ini tidak mengaktifkan sensor pengukuran langsung.
- RECOVERY: `-- H`. Forerunner 45 tidak menyediakan data ini melalui API watch face. Angka nol tidak digunakan sebagai pengganti data yang tidak tersedia.
- KCAL: kalori total hari ini yang dilaporkan perangkat.
- Lengkung bawah: hiasan mengikuti referensi; isian titik dan persentase menunjukkan progres target langkah. Angka 05:30 pada referensi tidak disalin sebagai data palsu.

Latar putih dan teks hitam dipilih supaya terbaca pada layar 8 warna FR45. Warna merah muda pucat pada foto tidak tersedia pada palet asli jam ini.

## Status

**SATISFY-FR45.prg berhasil dikompilasi menggunakan Garmin Connect IQ SDK 9.2.0 dan profil resmi fr45 (API 1.4.5).** Versi debug berhasil dijalankan pada simulator Forerunner 45; waktu berubah, teks SATISFY serta seluruh baris terlihat, dan penggunaan memori yang teramati sekitar 8,8 KiB dari batas 48 KiB. Tidak terlihat error runtime selama pemeriksaan ini.

Paket pemasangan berisi hasil kompilasi release. Pengujian pada jam fisik belum dilakukan. Pengujian ini belum memverifikasi seluruh kemungkinan nilai sensor atau perubahan tanggal. RECOVERY tetap `-- H` sesuai keterbatasan perangkat.

Gambar pada folder output adalah **pratinjau desain dengan angka contoh**, bukan tangkapan simulator. Jangan mengganti ekstensi gambar atau ZIP menjadi `.prg`.

## Membangun file PRG

1. Buka Garmin Connect IQ SDK Manager resmi: https://developer.garmin.com/connect-iq/sdk/
2. Masuk sendiri dengan akun Garmin Anda. Jangan kirim kata sandi melalui chat.
3. Pada tab SDKs, unduh SDK lalu aktifkan.
4. Pada tab Devices, unduh **Forerunner 45** (ID `fr45`).
5. Jalankan dari PowerShell 7 pada folder proyek:

   ```powershell
   ./tools/build.ps1
   ```

   Bila lokasi SDK berbeda:

   ```powershell
   ./tools/build.ps1 -SdkPath 'C:\lokasi\sdk' -JavaPath 'C:\lokasi\java.exe'
   ```

Hasil kompilasi: `output/SATISFY-FR45.prg`. Skrip membuat kunci pengembang lokal di `.private/` jika belum ada. Simpan folder itu untuk membangun pembaruan; jangan membagikannya.

## Menguji

1. Jalankan simulator Connect IQ dari SDK yang dipakai.
2. Bangun versi debug dengan `./tools/build.ps1 -DebugBuild`.
3. Jalankan `monkeydo output/SATISFY-FR45.prg fr45` dari terminal yang memiliki Java dan SDK di PATH.
4. Periksa tampilan jam, pergantian hari, pengaturan waktu 12/24 jam, baterai, langkah, target, jarak, kalori, serta kondisi riwayat detak jantung kosong.
5. Periksa bahwa penggunaan memori di bawah 48 KiB dan tidak ada error runtime. Setelah itu bangun ulang tanpa `-DebugBuild` untuk berkas pemasangan.

## Memasang PRG yang disertakan

1. Sambungkan FR45 ke komputer memakai kabel USB data.
2. Salin `SATISFY-FR45.prg` ke folder `GARMIN/APPS` pada jam.
3. Eject perangkat dengan aman, lalu cabut kabel.
4. Tahan UP pada jam, pilih Watch Face, pilih SATISFY FR45, lalu terapkan.

Gunakan file hasil target `fr45`; file untuk Forerunner 55 tidak otomatis kompatibel.

## Struktur proyek

- `source/`: kode Monkey C.
- `resources/`: ikon dan font bitmap kecil.
- `tools/build.ps1`: kompilasi dengan SDK resmi.
- `tools/make_assets.py`: pembuatan font dan pratinjau; membutuhkan Pillow dan font Arial Windows. Aset sudah disertakan sehingga tidak perlu dijalankan untuk kompilasi.
- `output/`: pratinjau, kemudian PRG jika kompilasi berhasil.

Rujukan: dokumentasi lokal SDK Garmin serta https://developer.garmin.com/connect-iq/api-docs/Toybox/ActivityMonitor/Info.html dan https://developer.garmin.com/connect-iq/api-docs/Toybox/ActivityMonitor.html.

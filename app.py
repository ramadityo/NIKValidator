import streamlit as st
import re
import pandas as pd

st.write("""
# NIK Validator 🔍
Selamat datang di aplikasi NIK Validator! Aplikasi ini dikhususkan untuk validasi dasar NIK Indonesia untuk wilayah Tangerang Selatan.
""")

def evaluasi_bagian(label, value, pola, bobot):
    if re.match(pola, value):
        return bobot, None
    else:
        return 0, f"Kesalahan pada {label}: {value}"

def proses_nik(input_nik):
    total_akurasi = 0
    pesan_error = []

    provinsi = input_nik[:2]
    kabupaten = input_nik[2:4]
    kecamatan = input_nik[4:6]
    tanggal_lahir = input_nik[6:8]
    bulan_lahir = input_nik[8:10]
    tahun_lahir = input_nik[10:12]
    nomor_unik = input_nik[12:]

    akurasi, error = evaluasi_bagian("Kode Provinsi", provinsi, rf'{KODE_PROVINSI:02d}', BOBOT["provinsi"])
    total_akurasi += akurasi
    if error: pesan_error.append(error)

    akurasi, error = evaluasi_bagian("Kode Kabupaten", kabupaten, rf'{KODE_KABUPATEN:02d}', BOBOT["kabupaten"])
    total_akurasi += akurasi
    if error: pesan_error.append(error)

    akurasi, error = evaluasi_bagian("Kode Kecamatan", kecamatan, rf'(?:' + '|'.join(KODE_KECAMATAN) + r')', BOBOT["kecamatan"])
    total_akurasi += akurasi
    if error: pesan_error.append(error)

    akurasi, error = evaluasi_bagian("Tanggal Lahir", tanggal_lahir + bulan_lahir + tahun_lahir, r'\d{6}', BOBOT["tanggal_lahir"])
    total_akurasi += akurasi
    if error: pesan_error.append(error)

    akurasi, error = evaluasi_bagian("Nomor Unik", nomor_unik, r'\d{4}', BOBOT["nomor_unik"])
    total_akurasi += akurasi
    if error: pesan_error.append(error)

    return total_akurasi, pesan_error

# Kita mengambil kode provinsi Banten dan kabupaten Tangerang
# Sumber dari Wikipedia
# https://id.wikipedia.org/wiki/Daftar_kecamatan_dan_kelurahan_di_Kota_Tangerang_Selatan
KODE_PROVINSI = 36
KODE_KABUPATEN = 74

NAMA_KECAMATAN = ["Serpong", "S. Utara", "P. Aren", "Ciputat", "C. Timur", "Pamulang", "Setu" ]
KODE_KECAMATAN = ["01", "02", "03", "04", "05", "06", "07"]

BOBOT = {
    "provinsi": 30,
    "kabupaten": 20,
    "kecamatan": 20,
    "tanggal_lahir": 20,
    "nomor_unik": 10,
}

input_nik = st.text_input("Masukkan NIK: ")

POLA_VALIDASI = rf'^{KODE_PROVINSI:02d}{KODE_KABUPATEN:02d}(' + '|'.join(KODE_KECAMATAN) + r')(\d{2})(\d{2})(\d{2})(\d{4})$'


if input_nik:
    total_akurasi, pesan_error = proses_nik(input_nik)

    if total_akurasi == 100:
        st.write("### Informasi NIK: VALID ✅")
        st.write(f"Akurasi NIK: {total_akurasi}%")
    else:
        st.write("### Informasi NIK: TIDAK VALID ❌")
        for error in pesan_error:
            st.error(error)
        st.write(f"### Akurasi NIK: {total_akurasi}%")


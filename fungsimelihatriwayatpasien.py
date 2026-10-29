import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

conn = sqlite3.connect("prediksi_diabetes.db")
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS pasien (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_pasien TEXT,
    usia INTEGER,
    gula_darah REAL,
    bmi REAL,
    riwayat_ortu TEXT,
    hasil_prediksi TEXT)""")

conn.commit()

def prediksi(gula, bmi, riwayat):
    if gula >= 200:
        if bmi >= 30 or riwayat == "Ya":
            return "Sangat Tinggi"
        return "Tinggi"

    elif gula >= 140:
        if bmi >= 30 or riwayat == "Ya":
            return "Tinggi"
        return "Sedang"

    else:
        if bmi >= 30:
            if riwayat == "Ya":
                return "Sedang"
            return "Waspada"

        if riwayat == "Ya":
            return "Waspada"

        return "Rendah"

    def proses():
    nama = entry_nama.get().strip()
    usia = entry_usia.get().strip()
    gula = entry_gula.get().strip()
    bmi = entry_bmi.get().strip()
    riwayat = combo_riwayat.get()

        # Validasi input kosong
    if nama == "" or usia == "" or gula == "" or bmi == "" or riwayat == "":
        messagebox.showwarning(
            "Peringatan",
            "Semua data harus diisi!"
        )
        return

    # Validasi usia
    if not usia.isdigit() or int(usia) < 1 or int(usia) > 120:
        messagebox.showwarning(
            "Peringatan",
            "Usia harus angka 1 - 120!"
        )
        return

        try:
        gula = float(gula)
        bmi = float(bmi)
    except ValueError:
        messagebox.showwarning(
            "Peringatan",
            "Gula darah dan BMI harus berupa angka!"
        )
        return

    if gula <= 0 or bmi <= 0:
        messagebox.showwarning(
            "Peringatan",
            "Gula darah dan BMI harus lebih dari 0!"
        )
        return

        hasil = prediksi(gula, bmi, riwayat)

    cur.execute(
        """INSERT INTO pasien
        (nama_pasien, usia, gula_darah, bmi, riwayat_ortu, hasil_prediksi)
        VALUES (?, ?, ?, ?, ?, ?)""",
        (nama, int(usia), gula, bmi, riwayat, hasil)
    )

    conn.commit()

        warna = {
        "Rendah": "green",
        "Waspada": "gold",
        "Sedang": "orange",
        "Tinggi": "red",
        "Sangat Tinggi": "darkred"
    }

    label_hasil.config(
        text="Risiko: " + hasil,
        bg=warna[hasil],
        fg="white"
    )

    def lihat_data():
    jendela = tk.Toplevel(root)
    jendela.title("Riwayat Pasien")


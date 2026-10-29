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


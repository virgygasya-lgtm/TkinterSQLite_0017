
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# 1. Koneksi database
conn = sqlite3.connect("prediksi_diabetes.db")
cur = conn.cursor()

# 2. Membuat tabel pasien
cur.execute("""
CREATE TABLE IF NOT EXISTS pasien (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_pasien TEXT,
    usia INTEGER,
    gula_darah REAL,
    bmi REAL,
    riwayat_ortu TEXT,
    hasil_prediksi TEXT
)
""")
conn.commit()


# 3. Fungsi prediksi diabetes
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


# 4. Fungsi proses input dan prediksi
def proses():
    nama = entry_nama.get().strip()
    usia = entry_usia.get().strip()
    gula = entry_gula.get().strip()
    bmi = entry_bmi.get().strip()
    riwayat = combo_riwayat.get()

    # Validasi data kosong
    if not nama or not usia or not gula or not bmi or not riwayat:
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

    # Validasi gula darah dan BMI
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

    # Menghitung hasil prediksi
    hasil = prediksi(gula, bmi, riwayat)

    # Menyimpan data pasien ke database
    cur.execute("""
        INSERT INTO pasien
        (nama_pasien, usia, gula_darah, bmi,
         riwayat_ortu, hasil_prediksi)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nama, int(usia), gula, bmi, riwayat, hasil))

    conn.commit()

    # Menampilkan hasil prediksi dengan warna
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

    messagebox.showinfo(
        "Berhasil",
        "Data pasien berhasil disimpan!"
    )


# 5. Fungsi melihat riwayat pasien
def lihat_data():
    jendela = tk.Toplevel(root)
    jendela.title("Riwayat Pasien")
    jendela.geometry("850x300")

    kolom = (
        "id",
        "nama_pasien",
        "usia",
        "gula_darah",
        "bmi",
        "riwayat_ortu",
        "hasil_prediksi"
    )

    tabel = ttk.Treeview(
        jendela,
        columns=kolom,
        show="headings"
    )

    # Membuat judul kolom
    judul_kolom = {
        "id": "ID",
        "nama_pasien": "Nama Pasien",
        "usia": "Usia",
        "gula_darah": "Gula Darah",
        "bmi": "BMI",
        "riwayat_ortu": "Riwayat Ortu",
        "hasil_prediksi": "Hasil Prediksi"
    }

    for k in kolom:
        tabel.heading(k, text=judul_kolom[k])
        tabel.column(k, width=115, anchor="center")

    tabel.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    # Mengambil data dari database
    cur.execute("SELECT * FROM pasien")

    for baris in cur.fetchall():
        tabel.insert("", tk.END, values=baris)


# 6. Membuat tampilan GUI
root = tk.Tk()
root.title("Prediksi Risiko Diabetes")
root.geometry("430x390")
root.resizable(False, False)

# Judul aplikasi
tk.Label(
    root,
    text="Prediksi Risiko Diabetes",
    font=("Arial", 16, "bold")
).grid(
    row=0,
    column=0,
    columnspan=2,
    pady=15
)

# Input nama pasien
tk.Label(root, text="Nama Pasien").grid(
    row=1, column=0, padx=10, pady=5, sticky="w"
)
entry_nama = tk.Entry(root, width=25)
entry_nama.grid(row=1, column=1, padx=10, pady=5)

# Input usia
tk.Label(root, text="Usia").grid(
    row=2, column=0, padx=10, pady=5, sticky="w"
)
entry_usia = tk.Entry(root, width=25)
entry_usia.grid(row=2, column=1, padx=10, pady=5)

# Input gula darah
tk.Label(root, text="Gula Darah (mg/dL)").grid(
    row=3, column=0, padx=10, pady=5, sticky="w"
)
entry_gula = tk.Entry(root, width=25)
entry_gula.grid(row=3, column=1, padx=10, pady=5)

# Input BMI
tk.Label(root, text="BMI").grid(
    row=4, column=0, padx=10, pady=5, sticky="w"
)
entry_bmi = tk.Entry(root, width=25)
entry_bmi.grid(row=4, column=1, padx=10, pady=5)

# Pilihan riwayat diabetes orang tua
tk.Label(root, text="Riwayat Diabetes Ortu").grid(
    row=5, column=0, padx=10, pady=5, sticky="w"
)
combo_riwayat = ttk.Combobox(
    root,
    values=["Ya", "Tidak"],
    state="readonly",
    width=22
)
combo_riwayat.grid(row=5, column=1, padx=10, pady=5)

# Tombol prediksi
tk.Button(
    root,
    text="Prediksi",
    width=12,
    command=proses
).grid(row=6, column=0, pady=15)

# Tombol lihat data
tk.Button(
    root,
    text="Lihat Data",
    width=12,
    command=lihat_data
).grid(row=6, column=1, pady=15)

# Label hasil prediksi
label_hasil = tk.Label(
    root,
    text="Hasil prediksi",
    font=("Arial", 12, "bold"),
    width=30,
    height=2,
    bg="lightgray"
)
label_hasil.grid(
    row=7,
    column=0,
    columnspan=2,
    padx=10,
    pady=5
)


# 7. Menjalankan aplikasi
def tutup_aplikasi():
    conn.close()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", tutup_aplikasi)
root.mainloop()



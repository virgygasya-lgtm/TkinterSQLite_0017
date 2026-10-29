import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

conn = sqlite3.connect("prediksi_diabetes.db")
cur = conn.cursor()


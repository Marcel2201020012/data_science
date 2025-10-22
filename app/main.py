import joblib
import tkinter as tk
from tkinter import font
import numpy as np

knn_model = joblib.load("model/knn.pkl")
regresi_linier_model = joblib.load("model/regresi_linier.pkl")
ensemble_model = joblib.load("model/ensemble.pkl")
z_scale = joblib.load('z_scale.pkl')

def format_rupiah(n):
    return "Rp {:,}".format(int(n)).replace(",", ".")

def clear_result():
    result_label.config(text="", fg="#2c3e50")

def prediksi_harga():
    clear_result()
    try:
        kamar_tidur = float(entries[0].get())
        kamar_mandi = float(entries[1].get())
        garasi = float(entries[2].get())
        luas_tanah = float(entries[3].get())
        luas_bangunan = float(entries[4].get())

        errors = []
        if luas_tanah <= 0 or luas_bangunan <= 0:
            errors.append("Luas tanah & bangunan harus > 0")
        if kamar_tidur < 0 or kamar_mandi < 0 or garasi < 0:
            errors.append("Jumlah kamar & garasi tidak boleh negatif")

        if errors:
            result_label.config(text=" • ".join(errors), fg="#e74c3c")
            return

        ft1 = np.log1p(kamar_tidur)
        ft2 = np.log1p(kamar_mandi)
        ft3 = np.log1p(garasi)
        ft4 = np.log(luas_tanah)
        ft5 = np.log(luas_bangunan)

        log_features = np.array([[ft1, ft2, ft3, ft4, ft5]])
        scaled_features = z_scale.transform(log_features)

        knn_pred = knn_model.predict(scaled_features)
        lr_pred = regresi_linier_model.predict(scaled_features)
        meta_input = np.column_stack((knn_pred, lr_pred))
        final_pred_log = ensemble_model.predict(meta_input)[0]
        predicted_price = np.exp(final_pred_log)
        result = int(np.round(predicted_price))

        result_label.config(text=f"Prediksi Harga Rumah: {format_rupiah(result)}", fg="#27ae60")

    except ValueError:
        result_label.config(text="Masukkan angka valid di semua kolom.", fg="#e74c3c")
    except Exception as e:
        result_label.config(text=f"Error: {type(e).__name__}", fg="#e74c3c")

#gui
root = tk.Tk()
root.title("Prediksi Harga Rumah Metode KNN + Regresi Linier")
root.geometry("600x500")
root.minsize(400, 400)
root.configure(bg="#f5f7fa")

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# font
title_font = font.Font(family="Segoe UI", size=16, weight="bold")
label_font = font.Font(family="Segoe UI", size=11)
entry_font = font.Font(family="Segoe UI", size=10)
button_font = font.Font(family="Segoe UI", size=11, weight="bold")
result_font = font.Font(family="Segoe UI", size=12, weight="bold")

# header
header_frame = tk.Frame(root, bg="#2c3e50", height=80)
header_frame.grid(row=0, column=0, sticky="ew")
header_frame.grid_columnconfigure(0, weight=1)

title_label = tk.Label(
    header_frame,
    text="Prediksi Harga Rumah\nKNN + Regresi Linier",
    font=title_font,
    fg="white",
    bg="#2c3e50",
    justify="center"
)
title_label.grid(row=0, column=0, pady=15, sticky="ew")

#input
input_frame = tk.Frame(root, bg="#f5f7fa", padx=20, pady=20)
input_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))
input_frame.grid_columnconfigure(1, weight=1)

labels = [
    "🛌 Kamar Tidur",
    "🚿 Kamar Mandi",
    "🚗 Garasi",
    "📐 Luas Tanah (m²)",
    "🏠 Luas Bangunan (m²)"
]

entries = []
for i, text in enumerate(labels):
    label = tk.Label(
        input_frame,
        text=text,
        font=label_font,
        bg="#f5f7fa",
        anchor="w"
    )
    label.grid(row=i, column=0, sticky="w", padx=(0, 10), pady=6)

    entry = tk.Entry(
        input_frame,
        font=entry_font,
        relief="flat",
        bg="#ecf0f1",
        justify="right"
    )
    entry.grid(row=i, column=1, sticky="ew", ipady=4, pady=6)
    entries.append(entry)

# tombol
predict_btn = tk.Button(
    root,
    text="Lihat Prediksi",
    command=prediksi_harga,
    font=button_font,
    bg="#3498db",
    fg="white",
    relief="flat",
    cursor="hand2",
    activebackground="#2980b9",
    activeforeground="white"
)
predict_btn.grid(row=2, column=0, pady=10, padx=20, sticky="ew")

# output
result_frame = tk.Frame(root, bg="#f5f7fa")
result_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 10))
result_frame.grid_columnconfigure(0, weight=1)

result_label = tk.Label(
    result_frame,
    text="",
    font=result_font,
    bg="#f5f7fa",
    fg="#2c3e50",
    wraplength=500,
    justify="center"
)
result_label.grid(row=0, column=0, sticky="ew")

def update_wraplength(event):
    new_wrap = int(root.winfo_width() * 0.9)
    result_label.config(wraplength=new_wrap)

root.bind("<Configure>", update_wraplength)

# footer
footer = tk.Label(
    root,
    text="Masukkan data rumah Anda untuk mendapatkan estimasi harga",
    font=("Segoe UI", 9),
    bg="#f5f7fa",
    fg="#7f8c8d"
)
footer.grid(row=4, column=0, pady=(0, 10), sticky="s")

root.grid_rowconfigure(4, weight=0)
root.grid_rowconfigure(3, weight=0)
root.grid_rowconfigure(2, weight=0)
root.grid_rowconfigure(1, weight=1)

root.bind('<Return>', lambda event: prediksi_harga())

root.mainloop()
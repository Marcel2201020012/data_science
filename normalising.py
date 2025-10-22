import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import joblib
from scipy.stats.mstats import winsorize
from sklearn.preprocessing import StandardScaler

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)

z_scale = StandardScaler()

#input
try:
    # data_frame = pd.read_csv("data/cleaning/hapus_duplikat.csv")
    # data_frame = pd.read_csv("data/normalising/hapus_outlier.csv")
    # data_frame = pd.read_csv("data/normalising/normalisasi_log.csv")
    data_frame = pd.read_csv("data/normalising/normalisasi_winsorize.csv")
    # data_frame = pd.read_csv("data/normalising/standarisasi_z_score.csv")
except Exception as err:
    print(err)

#cek distribusi, kalau tidak normal tidak bisa pakai z-score methode untuk cek outlier
# kolom = data_frame.select_dtypes(include=np.number).columns
# jumlah_kolom = len(kolom)
# baris = int(np.ceil(jumlah_kolom / 3))  # 3 grafik per baris

# plt.figure(figsize=(10, 3 * baris))

# for i, kol in enumerate(kolom, 1):
#     plt.subplot(baris, 3, i)
#     sns.histplot(data_frame[kol], kde=True)
#     plt.title(f'Distribusi: {kol}')
#     plt.xlabel(kol)
#     plt.ylabel('Frekuensi')

# plt.tight_layout()
# plt.show()

#cek outlier, karena tidak normal maka pakai iqr
# Q1 = data_frame.quantile(0.25)
# Q3 = data_frame.quantile(0.75)
# IQR = Q3 - Q1
# outlier_mask = (data_frame < (Q1 - 1.5 * IQR)) | (data_frame > (Q3 + 1.5 * IQR))

# outliers = data_frame[outlier_mask.any(axis=1)]
# print(outliers)
# print("Total outliers: " + str(len(outliers)))

# data_frame.plot(kind='box', subplots=True, layout=(2,3), figsize=(12,8), sharex=False, sharey=False)
# plt.show()

#cek proporsi outlier tiap parameter
# for col in ['harga', 'jumlah_kamar_tidur', 'jumlah_kamar_mandi', 'jumlah_garasi', 'luas_tanah', 'luas_bangunan']:
#     Q1 = data_frame[col].quantile(0.25)
#     Q3 = data_frame[col].quantile(0.75)
#     IQR = Q3 - Q1
#     lower = Q1 - 1.5*IQR
#     upper = Q3 + 1.5*IQR
#     outlier_count = ((data_frame[col] < lower) | (data_frame[col] > upper)).sum()
#     print(f"{col}: {outlier_count} outliers ({outlier_count/len(data_frame)*100:.1f}%)")

#hapus outlier ekstrim (indeks 872 dengan luas bangunan 2.408.150.000)
# data_frame.drop(data_frame.index[872], inplace=True)
# data_frame.reset_index(drop=True, inplace=True)
# data_frame.to_html("output/normalising/hapus_outlier.html")
# data_frame.to_csv("data/normalising/hapus_outlier.csv", index=False)

#normalisasi parameter untuk meminimalkan outlier dengan log transform
data_frame['harga'] = np.log(data_frame['harga'])
data_frame['luas_tanah'] = np.log(data_frame['luas_tanah'])
data_frame['luas_bangunan'] = np.log(data_frame['luas_bangunan'])
data_frame['jumlah_kamar_tidur'] = np.log1p(data_frame['jumlah_kamar_tidur'])
data_frame['jumlah_kamar_mandi'] = np.log1p(data_frame['jumlah_kamar_mandi'])
data_frame['jumlah_garasi'] = np.log1p(data_frame['jumlah_garasi'])
# data_frame.to_csv("data/normalising/normalisasi_log.csv", index=False)
# data_frame.to_html("output/normalising/normalisasi_log.html")

#normalisasi winsorize 90% untuk meminimalkan outlier
# data_frame['harga'] = winsorize(data_frame['harga'], limits=(0.05, 0.05))
# data_frame['luas_tanah'] = winsorize(data_frame['luas_tanah'], limits=(0.05, 0.05))v
# data_frame['luas_bangunan'] = winsorize(data_frame['luas_bangunan'], limits=(0.05, 0.05))
# data_frame['jumlah_kamar_tidur'] = winsorize(data_frame['jumlah_kamar_tidur'], limits=(0.05, 0.05))
# data_frame['jumlah_kamar_mandi'] = winsorize(data_frame['jumlah_kamar_mandi'], limits=(0.05, 0.05))
# data_frame['jumlah_garasi'] = winsorize(data_frame['jumlah_garasi'], limits=(0.05, 0.05))
# data_frame.to_csv("data/normalising/normalisasi_winsorize.csv", index=False)
# data_frame.to_html("output/normalising/normlisasi_winsorize.html")

#standarisasi z-score
# kolom = ['luas_tanah', 'luas_bangunan', 'jumlah_kamar_tidur', 'jumlah_kamar_mandi', 'jumlah_garasi']
# data_frame[kolom] = z_scale.fit_transform(data_frame[kolom]) #fit transform untuk training, transform untuk testing
# joblib.dump(z_scale, 'z_scale.pkl')
# data_frame.to_csv("data/normalising/standarisasi_z_score.csv", index=False)
# data_frame.to_html("output/normalising/standarisasi_z_score.html")

# Inverse transform log dan standarisasi z-score (untuk mengembalikan nilai parameter)
# kolom = ['luas_tanah', 'luas_bangunan', 'jumlah_kamar_tidur', 'jumlah_kamar_mandi', 'jumlah_garasi']
# z_scale = joblib.load('z_scale.pkl')
# data_frame[kolom] = z_scale.inverse_transform(data_frame[kolom])

# data_frame['harga'] = np.exp(data_frame['harga'])
# data_frame['luas_tanah'] = np.exp(data_frame['luas_tanah'])
# data_frame['luas_bangunan'] = np.exp(data_frame['luas_bangunan'])
# data_frame['jumlah_kamar_tidur'] = np.expm1(data_frame['jumlah_kamar_tidur'])
# data_frame['jumlah_kamar_mandi'] = np.expm1(data_frame['jumlah_kamar_mandi'])
# data_frame['jumlah_garasi'] = np.expm1(data_frame['jumlah_garasi'])
# kolom = ["harga", "luas_tanah", "luas_bangunan", "jumlah_kamar_tidur", "jumlah_kamar_mandi", "jumlah_garasi"]
# data_frame[kolom] = data_frame[kolom].round().astype(int)

# data_frame.to_csv("output/invers.csv")
# data_frame.to_html("output/inverse.html")
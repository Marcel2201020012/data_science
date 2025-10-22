import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)

#input
try:
    data_frame = pd.read_csv("data/raw/raw.csv")
    # data_frame = pd.read_csv("data/cleaning/rename_kolom.csv")
    # data_frame = pd.read_csv("data/cleaning/hapus_kolom.csv")
    # data_frame = pd.read_csv("data/cleaning/fill_nan.csv")
    # data_frame = pd.read_csv("data/cleaning/ubah_tipe_data_harga.csv")
    # data_frame = pd.read_csv("data/cleaning/ubah_tipe_data_jumlah.csv")
    # data_frame = pd.read_csv("data/cleaning/ubah_tipe_data_luas.csv")
    # data_frame = pd.read_csv("data/cleaning/hapus_baris.csv")
    print(data_frame.head(1000))
    # print(len(data_frame))
    # print(data_frame.dtypes)
    # data_frame.to_html("output/raw/raw.html") 
except Exception as err:
    print(err)

#Ubah nama kolom 
# data_frame = data_frame.rename(columns={
#     'price': 'harga',
#     'nav-link': 'tautan',
#     'description': 'deskripsi',
#     'listing-location': 'lokasi',
#     'bed': 'jumlah_kamar_tidur',
#     'bath': 'jumlah_kamar_mandi',
#     'carport': 'jumlah_garasi',
#     'surface_area': 'luas_tanah',
#     'building_area': 'luas_bangunan'
# })
# data_frame.to_html("output/cleaning/rename.html") 
# data_frame.to_csv("data/cleaning/rename_kolom.csv", index=False)

#hapus kolom yang tidak relevan
# data_frame = data_frame.drop(['tautan', 'deskripsi', 'lokasi'], axis=1)
# data_frame.to_html("output/cleaning/hapus_kolom.html")
# data_frame.to_csv("data/cleaning/hapus_kolom.csv", index=False)

#menangani missing value
#kolom jumlah kamar, jumlah kamar mandi, dan garasi harusnya bernilai >=0, sehingga nilai NaN di kolom ini termasuk MNAR (Missing Not At Random)
# kolom = ["jumlah_kamar_tidur", "jumlah_kamar_mandi", "jumlah_garasi"]
# data_frame[kolom] = data_frame[kolom].fillna(0.0)
# data_frame.to_html("output/cleaning/fill_nan.html")
# data_frame.to_csv("data/cleaning/fill_nan.csv", index=False)

#ubah tipe data harga menjadi int
# def konversi(harga):
#     teks = str(harga).lower()
#     teks = teks.replace("rp", "").replace(" ", "").replace("\xa0", "")  # hapus Rp dan spasi
#     teks = teks.replace(".", "")
#     teks = teks.replace(",", ".")
    
#     multiplier = 1
#     if "miliar" in teks:
#         multiplier = 1_000_000_000
#         teks = teks.replace("miliar", "")
#     elif "juta" in teks:
#         multiplier = 1_000_000
#         teks = teks.replace("juta", "")
    
#     try:
#         num = float(teks.strip()) * multiplier
#         return int(round(num))
#     except ValueError:
#         return None
    
# data_frame["harga"] = data_frame["harga"].apply(konversi)
# data_frame.to_html("output/cleaning/ubah_tipe_data_harga.html")
# data_frame.to_csv("data/cleaning/ubah_tipe_data_harga.csv", index=False)

#mengubah tipe data jumlah kamar, kamar mandi, garasi ke int
# kolom = ["jumlah_kamar_tidur", "jumlah_kamar_mandi", "jumlah_garasi"]
# data_frame[kolom] = data_frame[kolom].astype(int)
# data_frame.to_html("output/cleaning/ubah_tipe_data_jumlah.html")
# data_frame.to_csv("data/cleaning/ubah_tipe_data_jumlah.csv", index=False)

#ubah tipe data luas jadi int
# def konversi(luas):
#     teks = str(luas).lower()
#     teks = teks.replace("m²", "").replace(" ", "").replace("\xa0", "")
#     try:
#         return int(teks)
#     except ValueError:
#         return 0

# kolom = ["luas_bangunan", "luas_tanah"]
# data_frame[kolom] = data_frame[kolom].applymap(konversi)
# data_frame.to_html("output/cleaning/ubah_tipe_data_luas.html")
# data_frame.to_csv("data/cleaning/ubah_tipe_data_luas.csv", index=False)

#hapus data kosong
# kolom_luas = ["luas_bangunan", "luas_tanah"]
# print("Hapus data:\n")
# print(data_frame[(data_frame[kolom_luas] == 0).all(axis=1)])
# data_frame = data_frame[~(data_frame[kolom_luas] == 0).all(axis=1)]
# data_frame.reset_index(drop=True, inplace=True)
# data_frame.to_html("output/cleaning/hapus_baris.html")
# data_frame.to_csv("data/cleaning/hapus_baris.csv", index=False)

# cek duplikat
# duplikat = data_frame[data_frame.duplicated()]
# print(duplikat)
# print("total duplikat:" + str(len(duplikat)))

# data_frame = data_frame.drop_duplicates(keep='first')
# data_frame.to_csv("data/cleaning/hapus_duplikat.csv", index=False)
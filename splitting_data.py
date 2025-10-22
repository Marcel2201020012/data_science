import pandas as pd
from sklearn.model_selection import train_test_split
import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler

z_scale = StandardScaler()

try:
    data_frame = pd.read_csv("data/normalising/normalisasi_winsorize.csv")
except Exception as err:
    print(err)

# Split data menjadi train (80%) dan remaining (20%)
data_frame_train, data_frame_remaining = train_test_split(
    data_frame,
    test_size=0.2,
    random_state=42,
    shuffle=True
)

# Split menjadi test (15%) dan validation (5%)
data_frame_test, data_frame_val = train_test_split(
    data_frame_remaining,
    test_size=1/20,
    random_state=42,
    shuffle=True
)

kolom = ['jumlah_kamar_tidur', 'jumlah_kamar_mandi', 'jumlah_garasi', 'luas_tanah', 'luas_bangunan']
data_frame_train[kolom] = z_scale.fit_transform(data_frame_train[kolom]) #fit transform untuk training, transform untuk testing
joblib.dump(z_scale, 'z_scale.pkl')
data_frame_train.to_csv("data/model_data/train.csv", index=False)
data_frame_train.to_html("output/model_data/train.html")

data_frame_test[kolom] = z_scale.transform(data_frame_test[kolom]) #ganti fit transform ke transform karena untuk testing
data_frame_test.to_csv("data/model_data/test.csv", index=False)
data_frame_test.to_html("output/model_data/test.html")

data_frame_val['harga'] = np.exp(data_frame_val['harga'])
data_frame_val['luas_tanah'] = np.exp(data_frame_val['luas_tanah'])
data_frame_val['luas_bangunan'] = np.exp(data_frame_val['luas_bangunan'])
data_frame_val['jumlah_kamar_tidur'] = np.expm1(data_frame_val['jumlah_kamar_tidur'])
data_frame_val['jumlah_kamar_mandi'] = np.expm1(data_frame_val['jumlah_kamar_mandi'])
data_frame_val['jumlah_garasi'] = np.expm1(data_frame_val['jumlah_garasi'])
kolom = ["harga", "jumlah_kamar_tidur", "jumlah_kamar_mandi", "jumlah_garasi", "luas_tanah", "luas_bangunan"]
data_frame_val[kolom] = data_frame_val[kolom].round().astype(int)
data_frame_val.to_csv("data/model_data/val.csv", index=False)
data_frame_val.to_html("output/model_data/val.html")
import pandas as pd
import joblib

z_scale = joblib.load("z_scale.pkl")

print(z_scale.feature_names_in_)

# try:
#     data_frame = pd.read_csv("output/y_test.csv")
#     # print(len(data_frame))
# except Exception as err:
#     print(err)

# print(data_frame["harga"].describe())
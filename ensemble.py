import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, median_absolute_error
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

try:
    first_level_train = pd.read_csv("data/model_data/train.csv")
    first_level_test = pd.read_csv("data/model_data/test.csv")
except Exception as err:
    print(err)

#variabel dependen adalah kolom harga
kolom = "harga"
y_train = first_level_train[kolom].values
x_train = first_level_train.drop(columns=[kolom]).values
y_test = first_level_test[kolom].values
x_test = first_level_test.drop(columns=[kolom]).values

#first level model dan meta model
first_learner_models = [
    ("knn", KNeighborsRegressor(n_neighbors=9)),
    ("regresi_linier", LinearRegression())
]
meta_model = LinearRegression()

#k-fold cross-validation untuk membuat dataset meta model
kf = KFold(n_splits=5, shuffle=True, random_state=42)
meta_features = np.zeros((len(x_train), len(first_learner_models)))

for i, (name, model) in enumerate(first_learner_models):
    fold_preds = np.zeros(len(x_train))
    
    for train_idx, val_idx in kf.split(x_train):
        X_tr, X_val = x_train[train_idx], x_train[val_idx]
        y_tr, y_val = y_train[train_idx], y_train[val_idx]
        
        model.fit(X_tr, y_tr)
        preds = model.predict(X_val)
        fold_preds[val_idx] = preds
    
    meta_features[:, i] = fold_preds
    model.fit(x_train, y_train)
    joblib.dump(model, f"model/{name}.pkl")

# Dataset meta model
meta_x_train = meta_features
meta_y_train = y_train

# Gabungkan meta-features dengan target
meta_train_df = pd.DataFrame(meta_x_train, columns=[name for name, _ in first_learner_models])
meta_train_df.insert(0, "target", meta_y_train)

# Simpan ke file CSV
meta_train_df.to_csv("data/model_data/meta_train.csv", index=False)
meta_train_df.to_html("output/model_data/meta_train.html")

#latih meta model
meta_model.fit(meta_x_train, meta_y_train)

#export model
joblib.dump(meta_model, "model/ensemble.pkl")

# Untuk prediksi pada test set
meta_x_test = np.column_stack([
    joblib.load(f"model/{name}.pkl").predict(x_test)
    for name, _ in first_learner_models
])

# Prediksi final dengan meta model
final_preds = meta_model.predict(meta_x_test)

# # invers transform data ke skala awal
y_pred_original = np.exp(final_preds)
y_pred = np.round(y_pred_original).astype(int)

y_test_original = np.exp(y_test)
y_test = np.round(y_test_original).astype(int)

y_pred_df = pd.DataFrame(y_pred, columns=['harga'])
y_pred_df.insert(0, "target", y_test)
y_pred_df.to_csv('y_pred.csv', index=False)

#evaluasi RMSE
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"RMSE: {rmse:,.2f}")

# MAE
mae = mean_absolute_error(y_test, y_pred)
print(f"MAE:  {mae:,.2f}")

# R^2
r2 = r2_score(y_test, y_pred)
print(f"R²:   {r2:.4f}")

# Median Absolute Error
medae = median_absolute_error(y_test, y_pred)
print(f"Median AE: {medae:,.2f}")

# Mape
mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
print(f"MAPE: {mape:.2f}%")

#mdape
mdape = np.median(np.abs((y_test - y_pred) / y_test)) * 100
print(f"MdAPE: {mdape:.2f}%")

#evaluasi error scatter plot
plt.figure(figsize=(8,6))
sns.scatterplot(x=y_test, y=y_pred, alpha=0.6)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', label='Prediksi Sempurna')
plt.xlabel("Harga Asli")
plt.ylabel("Harga Prediksi")
plt.title("Scatter Plot Harga Prediksi & Asli")
plt.legend()
plt.show()

errors = y_pred - y_test

#evaluasi distribusi error
plt.figure(figsize=(8,6))
sns.histplot(errors, bins=50, kde=True)
plt.xlabel("Prediksi Error")
plt.title("Distribusi Error")
plt.show()

#evaluasi boxplot error
plt.figure(figsize=(6,4))
sns.boxplot(x=errors)
plt.title("Boxplot Prediksi Error")
plt.show()
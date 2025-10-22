import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, median_absolute_error
import joblib

def evaluate_model(model, X_train, X_test, y_train, y_test, model_name):
    model.fit(X_train, y_train)
    final_preds = model.predict(X_test)

    y_pred_original = np.exp(final_preds)
    y_pred = np.round(y_pred_original).astype(int)

    y_test_original = np.exp(y_test)
    y_test = np.round(y_test_original).astype(int)

    # y_test_df = pd.DataFrame(y_test, columns=['harga'])
    # y_test_df.to_csv('y_test.csv', index=False)
    
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    med_ae = median_absolute_error(y_test, y_pred)
    
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
    mdape = np.median(np.abs((y_test - y_pred) / y_test)) * 100
    
    print(f"\n=== {model_name} ===")
    print(f"RMSE: {rmse:,.2f}")
    print(f"MAE:  {mae:,.2f}")
    print(f"R²:   {r2:.4f}")
    print(f"Median AE: {med_ae:,.2f}")
    print(f"MAPE: {mape:.2f}%")
    print(f"MdAPE: {mdape:.2f}%")
    
    return {
        'Model': model_name,
        'RMSE': rmse,
        'MAE': mae,
        'R2': r2,
        'Median_AE': med_ae,
        'MAPE': mape,
        'MdAPE': mdape
    }

try:
    first_level_train = pd.read_csv("data/model_data/train.csv")
    first_level_test = pd.read_csv("data/model_data/test.csv")
except Exception as err:
    print(err)

kolom = "harga"
y_train = first_level_train[kolom].values
x_train = first_level_train.drop(columns=[kolom]).values
y_test = first_level_test[kolom].values
x_test = first_level_test.drop(columns=[kolom]).values

z_scale = joblib.load('z_scale.pkl')

knn = KNeighborsRegressor(n_neighbors=9)
knn_results = evaluate_model(knn, x_train, x_test, y_train, y_test, "KNN")

lr = LinearRegression()
lr_results = evaluate_model(lr, x_train, x_test, y_train, y_test, "Linear Regression")
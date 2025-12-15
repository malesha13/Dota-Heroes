import pandas as pd
import os

print("=== ПРОСТОЙ ТЕСТ ЗАГРУЗКИ ===")

print("Текущая папка:", os.getcwd())

try:
    print("\nПробуем загрузить X_features.csv...")
    X = pd.read_csv('ml_data/X_features.csv')
    print(f"✅ Успешно! Размер: {X.shape}")

    print("\nПервые 5 строк:")
    print(X.head())

except Exception as e:
    print(f"❌ Ошибка: {e}")

    print("\nПробуем другой путь...")
    try:
        X = pd.read_csv('./ml_data/X_features.csv')
        print(f"✅ Успешно с ./ ! Размер: {X.shape}")
    except Exception as e2:
        print(f"❌ Снова ошибка: {e2}")

print("\nПроверка завершена!")
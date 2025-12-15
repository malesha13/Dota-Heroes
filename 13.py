import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

print("=== ОБУЧЕНИЕ МОДЕЛИ НА ФАКТИЧЕСКИХ ДАННЫХ ===")

print("Загружаем данные...")
X = pd.read_csv('ml_data/X_features.csv')
y = pd.read_csv('ml_data/y_target.csv')

if '0' in y.columns:
    y = y['0']
else:
    y = y.iloc[:, 0]

print(f"Размер данных: {X.shape[0]} матчей")
print(f"Признаков: {X.shape[1]}")

print("Делим данные...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Обучаем на {len(X_train)} матчах")
print(f"Тестируем на {len(X_test)} матчах")

print("Обучаем модель...")
model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X_train, y_train)
print("Готово!")

print("Проверяем точность...")
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Точность: {acc:.3f} ({acc*100:.1f}%)")

print("Сохраняем модель...")
joblib.dump(model, 'models/dota_model.pkl')
print("Модель сохранена!")

print("Топ-5 важных героев:")
importance = pd.DataFrame({
    'hero': X.columns,
    'value': model.feature_importances_
}).sort_values('value', ascending=False)

for i in range(5):
    print(f"{i+1}. {importance.iloc[i]['hero']}")

print(f"Модель готова! Точность: {acc*100:.1f}%")
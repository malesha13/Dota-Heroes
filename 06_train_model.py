import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os
import sys

print("=== ОБУЧЕНИЕ МОДЕЛИ ===")

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ml_data_path = os.path.join(project_path, 'ml_data')
models_path = os.path.join(project_path, 'models')

print(f"Ищем данные в: {ml_data_path}")

if not os.path.exists(ml_data_path):
    print("❌ Папка ml_data не найдена!")
    print("Сначала запусти 05_prepare_ml_data.py")
    sys.exit(1)

if not os.path.exists(models_path):
    os.makedirs(models_path)

print("Загружаем данные...")
try:
    X_path = os.path.join(ml_data_path, 'X_features.csv')
    y_path = os.path.join(ml_data_path, 'y_target.csv')

    X = pd.read_csv(X_path)
    y_data = pd.read_csv(y_path)

    if '0' in y_data.columns:
        y = y_data['0']
    else:
        y = y_data.iloc[:, 0]

    print(f"✅ Данные загружены: {X.shape[0]} матчей")

except Exception as e:
    print(f"❌ Ошибка загрузки: {e}")
    sys.exit(1)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Обучающая: {X_train.shape[0]}")
print(f"Тестовая: {X_test.shape[0]}")

print("Обучаем модель...")
model = RandomForestClassifier(
    n_estimators=50,
    max_depth=8,
    random_state=42
)

model.fit(X_train, y_train)
print("✅ Модель обучена!")

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Точность: {accuracy:.3f}")

model_filename = os.path.join(models_path, 'dota_model.pkl')
joblib.dump(model, model_filename)
print(f"✅ Модель сохранена")

feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("Топ-5 важных героев:")
top_heroes = feature_importance.head(5)
for i, row in top_heroes.iterrows():
    print(f"  {row['feature']} - {row['importance']:.4f}")

print("Тест примеров:")
for i in range(min(2, len(X_test))):
    actual = "RADIANT" if y_test.iloc[i] == 1 else "DIRE"
    pred = "RADIANT" if y_pred[i] == 1 else "DIRE"
    correct = "✅" if y_test.iloc[i] == y_pred[i] else "❌"
    print(f"  Пример {i + 1}: {correct} {pred} vs {actual}")

print(f"🎉 Готово! Точность: {accuracy * 100:.1f}%")
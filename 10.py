import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

print("=== ОБУЧАЕМ МОДЕЛЬ НА РЕАЛЬНЫХ ДАННЫХ ===")

print("📊 Загружаем данные...")
X = pd.read_csv('ml_data/X_features.csv')
y_data = pd.read_csv('ml_data/y_target.csv')

print(f"✅ Данные загружены:")
print(f"   Матчей: {X.shape[0]}")
print(f"   Признаков: {X.shape[1]}")

if '0' in y_data.columns:
    y = y_data['0']
else:
    y = y_data.iloc[:, 0]

print(f"   Целевых значений: {len(y)}")

print("\n🎯 Делим на обучение и тест...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"   Обучающая выборка: {len(X_train)} матчей")
print(f"   Тестовая выборка: {len(X_test)} матчей")

print("\n🤖 Обучаем Random Forest...")
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)
print("✅ Модель обучена!")

print("\n📈 Оцениваем точность...")
y_pred_train = model.predict(X_train)
train_acc = accuracy_score(y_train, y_pred_train)

y_pred_test = model.predict(X_test)
test_acc = accuracy_score(y_test, y_pred_test)

print(f"   Точность на обучении: {train_acc:.3f} ({train_acc * 100:.1f}%)")
print(f"   Точность на тесте: {test_acc:.3f} ({test_acc * 100:.1f}%)")

baseline = max(y_test.mean(), 1 - y_test.mean())
print(f"   Базовая точность: {baseline:.3f} ({baseline * 100:.1f}%)")

if test_acc > baseline:
    print("   ✅ Модель лучше базового предсказания!")
else:
    print("   ⚠️  Нужно больше данных для улучшения")

print("\n💾 Сохраняем модель...")
if not os.path.exists('models'):
    os.makedirs('models')

joblib.dump(model, 'models/dota_predictor.pkl')
print("✅ Модель сохранена в models/dota_predictor.pkl")

print("\n🔍 Анализ важных признаков...")
importance_df = pd.DataFrame({
    'hero': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("Топ-10 самых влиятельных героев:")
for i in range(min(10, len(importance_df))):
    hero = importance_df.iloc[i]
    print(f"   {i + 1:2d}. {hero['hero']:40} - {hero['importance']:.4f}")

print("\n🎯 Тестируем на 3 примерах...")
correct = 0
for i in range(min(3, len(X_test))):
    actual = "RADIANT" if y_test.iloc[i] == 1 else "DIRE"
    predicted = "RADIANT" if y_pred_test[i] == 1 else "DIRE"

    if actual == predicted:
        correct += 1
        print(f"   ✅ Пример {i + 1}: Угадали ({predicted})")
    else:
        print(f"   ❌ Пример {i + 1}: Ошибка (сказали {predicted}, а победил {actual})")

print(f"\n🎉 МОДЕЛЬ ГОТОВА К ИСПОЛЬЗОВАНИЮ!")
print(f"📊 Итоговая точность: {test_acc * 100:.1f}%")
print(f"📊 Тестовые примеры: {correct}/3 правильных")

print("\nТеперь можно создавать Telegram-бота!")
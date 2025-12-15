import pandas as pd
import joblib

print("=== ФИНАЛЬНАЯ ПОДГОТОВКА БОТА ===")

print("1. Загружаем модель...")
model = joblib.load('models/dota_model.pkl')
print("   ✅ Модель загружена")

print("\n2. Загружаем героев...")
heroes = pd.read_csv('heroes.csv')
print(f"   ✅ Героев: {len(heroes)}")

print("\n3. Создаем перевод героев...")
id_to_name = {}
name_to_id = {}

for _, row in heroes.iterrows():
    hero_id = int(row['id'])
    hero_name = str(row['name'])
    id_to_name[hero_id] = hero_name
    name_to_id[hero_name] = hero_id

print(f"   ✅ Словарь создан")

print("\n4. Тестовая функция...")
all_ids = sorted(heroes['id'].unique().tolist())


def find_best_hero(ally_ids, enemy_ids):
    best = None
    best_score = 0

    for hero_id in all_ids:
        if hero_id in ally_ids or hero_id in enemy_ids:
            continue

        # Простая заглушка для теста
        # В реальном боте здесь будет вызов модели
        score = 50.0  # Заглушка 50%

        if score > best_score:
            best_score = score
            best = hero_id

    return best, best_score


print("\n5. Тест...")
test_ally = [1, 2]
test_enemy = [5, 6, 7]
hero_id, score = find_best_hero(test_ally, test_enemy)
hero_name = id_to_name.get(hero_id, f"ID {hero_id}")

print(f"   Союзники: {[id_to_name[i] for i in test_ally]}")
print(f"   Противники: {[id_to_name[i] for i in test_enemy]}")
print(f"   Рекомендуем: {hero_name}")
print(f"   Оценка: {score}%")

print("\n6. Сохраняем данные...")
import json

data = {
    'id_to_name': {str(k): v for k, v in id_to_name.items()},
    'name_to_id': name_to_id,
    'all_hero_ids': all_ids
}

with open('bot_config.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("   ✅ Данные сохранены в bot_config.json")

print("\n🎉 ВСЁ ГОТОВО ДЛЯ СОЗДАНИЯ БОТА!")
print("\nСледующие шаги:")
print("1. Создать бота через @BotFather")
print("2. Получить токен")
print("3. Написать код Telegram-бота")
print("4. Соединить бота с моделью")
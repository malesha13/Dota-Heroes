import pandas as pd
import joblib
import json
import warnings

print("=== ЧИСТАЯ ПОДГОТОВКА БОТА ===")

# Отключаем предупреждения
warnings.filterwarnings('ignore')

print("1. Загружаем модель...")
model = joblib.load('models/dota_model.pkl')
print("   ✅ Модель загружена")

print("\n2. Загружаем героев...")
heroes = pd.read_csv('heroes.csv')
print(f"   ✅ Героев: {len(heroes)}")

print("\n3. Создаем словари...")
id_to_name = {}
name_to_id = {}

for _, row in heroes.iterrows():
    hero_id = int(row['id'])
    hero_name = str(row['name'])
    id_to_name[hero_id] = hero_name
    name_to_id[hero_name] = hero_id

print(f"   ✅ Словари созданы")

print("\n4. Получаем все ID...")
all_ids = sorted(heroes['id'].unique().tolist())
print(f"   ✅ Всего ID: {len(all_ids)}")

print("\n5. Тестовая функция...")


def get_recommendation(ally_ids, enemy_ids):
    best_hero = None
    best_score = 0

    for hero_id in all_ids:
        if hero_id in ally_ids or hero_id in enemy_ids:
            continue

        # Заглушка для теста (в боте будет реальная модель)
        score = 50.0 + (hero_id % 20)  # Просто пример

        if score > best_score:
            best_score = score
            best_hero = hero_id

    return best_hero, best_score


print("\n6. Тестируем...")
test_ally = [1, 2, 3, 4]
test_enemy = [5, 6, 7, 8, 9]

hero_id, score = get_recommendation(test_ally, test_enemy)
hero_name = id_to_name.get(hero_id, f"Герой {hero_id}")

print(f"   Союзники: {[id_to_name[i] for i in test_ally]}")
print(f"   Противники: {[id_to_name[i] for i in test_enemy]}")
print(f"   Рекомендуем: {hero_name}")
print(f"   Оценка: {score:.1f}%")

print("\n7. Сохраняем конфиг для бота...")
config = {
    'id_to_name': {str(k): v for k, v in id_to_name.items()},
    'name_to_id': name_to_id,
    'all_hero_ids': all_ids
}

with open('bot_config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

print("   ✅ Конфиг сохранен в bot_config.json")

print("\n🎉 ВСЁ ГОТОВО!")
print("Теперь можно создавать Telegram-бота")
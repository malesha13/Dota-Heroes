
import json
import os
import pandas as pd
import numpy as np

print("=== ПОДГОТОВКА ДАННЫХ ДЛЯ МАШИННОГО ОБУЧЕНИЯ ===")


print("📁 Загружаем данные о героях...")
heroes_df = pd.read_csv('heroes.csv')
all_hero_ids = sorted(heroes_df['id'].unique())
print(f"✅ Всего героев: {len(all_hero_ids)}")


if not os.path.exists('ml_data'):
    os.makedirs('ml_data')


matches_folder = 'matches_data'
match_files = [f for f in os.listdir(matches_folder) if f.endswith('.json')]
print(f"📊 Будем обрабатывать {len(match_files)} матчей")


ml_data = []

print("\n🔧 Преобразуем матчи в формат для ML...")

for i, filename in enumerate(match_files):
    if i % 20 == 0:
        print(f"   Обработано {i}/{len(match_files)} матчей")

    filepath = os.path.join(matches_folder, filename)

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            match_data = json.load(f)


        players = match_data.get('players', [])
        if len(players) != 10:
            continue

        radiant_win = match_data.get('radiant_win')
        if radiant_win is None:
            continue


        radiant_heroes = []
        dire_heroes = []

        for player in players:
            hero_id = player.get('hero_id')
            if hero_id is None:
                continue

            if player.get('isRadiant'):
                radiant_heroes.append(hero_id)
            else:
                dire_heroes.append(hero_id)


        if len(radiant_heroes) != 5 or len(dire_heroes) != 5:
            continue


        features = []


        for hero_id in all_hero_ids:
            features.append(1 if hero_id in radiant_heroes else 0)


        for hero_id in all_hero_ids:
            features.append(1 if hero_id in dire_heroes else 0)

        target = 1 if radiant_win else 0

        ml_data.append({
            'features': features,
            'target': target,
            'radiant_heroes': radiant_heroes,
            'dire_heroes': dire_heroes,
            'match_id': match_data.get('match_id')
        })

    except Exception as e:
        continue

print(f"\n✅ УСПЕШНО ОБРАБОТАНО: {len(ml_data)} матчей")

if len(ml_data) == 0:
    print("❌ Не удалось обработать ни одного матча")
    exit()


print("\n📊 СОЗДАЕМ ТАБЛИЦУ ДЛЯ ML...")

feature_columns = []
for hero_id in all_hero_ids:
    hero_name = heroes_df[heroes_df['id'] == hero_id]['name'].iloc[0]
    feature_columns.append(f'radiant_{hero_id}_{hero_name}')

for hero_id in all_hero_ids:
    hero_name = heroes_df[heroes_df['id'] == hero_id]['name'].iloc[0]
    feature_columns.append(f'dire_{hero_id}_{hero_name}')


X = pd.DataFrame([item['features'] for item in ml_data], columns=feature_columns)
y = pd.Series([item['target'] for item in ml_data])


X.to_csv('ml_data/X_features.csv', index=False)
y.to_csv('ml_data/y_target.csv', index=False)


match_info = []
for item in ml_data:
    match_info.append({
        'match_id': item['match_id'],
        'radiant_heroes': ','.join(map(str, item['radiant_heroes'])),
        'dire_heroes': ','.join(map(str, item['dire_heroes'])),
        'radiant_win': item['target']
    })

pd.DataFrame(match_info).to_csv('ml_data/matches_info.csv', index=False)

print(f"\n🎉 ДАННЫЕ ПОДГОТОВЛЕНЫ!")
print(f"📁 Файлы сохранены в папку ml_data/")
print(f"   • X_features.csv - признаки для ML ({X.shape[1]} колонок)")
print(f"   • y_target.csv - целевая переменная ({len(y)} строк)")
print(f"   • matches_info.csv - информация о матчах")

print(f"\n📊 СТАТИСТИКА ДАННЫХ:")
print(f"   Всего записей: {len(ml_data)}")
print(f"   Признаков на запись: {X.shape[1]}")
print(f"   Побед Radiant: {sum(y)} ({sum(y) / len(y) * 100:.1f}%)")
print(f"   Побед Dire: {len(y) - sum(y)} ({(len(y) - sum(y)) / len(y) * 100:.1f}%)")

print(f"\n🔍 ПЕРВЫЕ 5 ПРИЗНАКОВ В ТАБЛИЦЕ:")
for col in X.columns[:5]:
    print(f"   {col}")

print(f"\n=== ДАННЫЕ ГОТОВЫ ДЛЯ ОБУЧЕНИЯ МОДЕЛИ ===")
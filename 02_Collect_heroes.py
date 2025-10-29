
import requests
import json
import pandas as pd

print("=== СОБИРАЕМ ДАННЫЕ О ГЕРОЯХ ===")


url = "https://api.opendota.com/api/heroes"
response = requests.get(url)

if response.status_code == 200:
    heroes = response.json()
    print(f"✅ Нашли {len(heroes)} героев")

    simple_heroes = []
    for hero in heroes:
        simple_heroes.append({
            'id': hero['id'],
            'name': hero['localized_name'],
            'primary_attr': hero['primary_attr'],  # str, agi, int
            'attack_type': hero['attack_type'],  # Melee или Ranged
            'roles': ', '.join(hero['roles'][:3])  # Первые 3 роли
        })

    df = pd.DataFrame(simple_heroes)
    df.to_csv('heroes.csv', index=False)
    print("✅ Сохранили heroes.csv")

    with open('heroes.json', 'w', encoding='utf-8') as f:
        json.dump(heroes, f, ensure_ascii=False, indent=2)
    print("✅ Сохранили heroes.json")

    print("\n📊 Статистика героев:")
    attr_count = df['primary_attr'].value_counts()
    for attr, count in attr_count.items():
        print(f"   {attr}: {count} героев")

    attack_count = df['attack_type'].value_counts()
    for attack, count in attack_count.items():
        print(f"   {attack}: {count} героев")

else:
    print("❌ Не удалось получить героев")

print("\n=== СОБРАЛИ ДАННЫЕ О ГЕРОЯХ ===")
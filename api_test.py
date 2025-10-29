
import requests

print("=== Начинаем тест API Dota 2 ===")

print("1. Получаем героев...")
url = "https://api.opendota.com/api/heroes"
response = requests.get(url)

if response.status_code == 200:
    heroes = response.json()
    print(f"✅ Успешно! Получили {len(heroes)} героев")

    print("Первые 5 героев:")
    for i in range(5):
        hero = heroes[i]
        print(f"   {hero['id']}: {hero['localized_name']}")
else:
    print(f"❌ Ошибка: {response.status_code}")


print("\n2. Получаем матчи...")
url_matches = "https://api.opendota.com/api/publicMatches?limit=5"
response_matches = requests.get(url_matches)

if response_matches.status_code == 200:
    matches = response_matches.json()
    print(f"✅ Успешно! Получили {len(matches)} матчей")

    for i, match in enumerate(matches):
        print(f"   Матч {i + 1}: ID {match['match_id']}")
else:
    print(f"❌ Ошибка: {response_matches.status_code}")

print("\n=== Тест завершен ===")
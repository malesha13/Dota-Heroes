
import requests
import time
import json
import os

print("=== НАЧИНАЕМ СОБИРАТЬ ДАННЫЕ О МАТЧАХ ===")
print("Это займет 2-3 минуты...")


if not os.path.exists('matches_data'):
    os.makedirs('matches_data')
    print("✅ Создана папка matches_data")


print("\n🔍 Ищем свежие матчи...")
url = "https://api.opendota.com/api/publicMatches?mmr_ascending=3000&limit=15"
response = requests.get(url)

if response.status_code != 200:
    print("❌ Ошибка: Не могу получить список матчей")
    exit()

matches_list = response.json()
print(f"✅ Нашли {len(matches_list)} матчей для анализа")

collected_count = 0
error_count = 0


for i, match in enumerate(matches_list):
    match_id = match['match_id']
    print(f"\n📊 Матч {i + 1}/{len(matches_list)} (ID: {match_id})")


    match_url = f"https://api.opendota.com/api/matches/{match_id}"
    match_response = requests.get(match_url)

    if match_response.status_code != 200:
        print("   ❌ Ошибка загрузки матча")
        error_count += 1
        continue

    match_data = match_response.json()


    players = match_data.get('players', [])
    if len(players) != 10:
        print("   ❌ В матче не 10 игроков - пропускаем")
        error_count += 1
        continue


    radiant_win = match_data.get('radiant_win')
    if radiant_win is None:
        print("   ❌ Неизвестен победитель - пропускаем")
        error_count += 1
        continue


    filename = f"matches_data/match_{match_id}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(match_data, f, ensure_ascii=False, indent=2)

    collected_count += 1


    duration = match_data.get('duration', 0) // 60  # переводим в минуты
    print(f"   ✅ Сохранен!")
    print(f"   ⏱️  Длительность: {duration} минут")
    print(f"   🏆 Победитель: {'RADIANT' if radiant_win else 'DIRE'}")


    radiant_heroes = []
    dire_heroes = []

    for player in players:
        hero_id = player.get('hero_id')
        if player.get('isRadiant'):
            radiant_heroes.append(hero_id)
        else:
            dire_heroes.append(hero_id)

    print(f"   👥 Radiant: {len(radiant_heroes)} героев")
    print(f"   👥 Dire: {len(dire_heroes)} героев")


    print("   ⏳ Ждем 1.5 секунды...")
    time.sleep(1.5)

print(f"\n🎉 СБОР ДАННЫХ ЗАВЕРШЕН!")
print(f"✅ Успешно собрано: {collected_count} матчей")
print(f"❌ Ошибок: {error_count} матчей")

if collected_count > 0:
    print(f"\n📁 Файлы сохранены в папку: matches_data/")
    print("Можно переходить к следующему шагу!")
else:
    print("\n😞 Не удалось собрать ни одного матча")
    print("Проверьте подключение к интернету")

print("\n=== ЗАВЕРШЕНО ===")

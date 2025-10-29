
import json
import os
import pandas as pd

print("=== АНАЛИЗИРУЕМ СОБРАННЫЕ МАТЧИ ===")
print(f"📁 Проверяем папку matches_data...")


matches_folder = 'matches_data'
if not os.path.exists(matches_folder):
    print("❌ Папка matches_data не найдена!")
    print("   Сначала запустите 03_collect_matches.py")
    exit()


match_files = [f for f in os.listdir(matches_folder) if f.endswith('.json')]
print(f"✅ Нашли {len(match_files)} файлов матчей")

if len(match_files) == 0:
    print("❌ В папке нет файлов матчей")
    exit()

print(f"\n📊 АНАЛИЗИРУЕМ {len(match_files)} МАТЧЕЙ...")


radiant_wins = 0
dire_wins = 0
total_duration = 0
match_durations = []
players_per_match = []


for i, filename in enumerate(match_files):
    filepath = os.path.join(matches_folder, filename)

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            match_data = json.load(f)


        if match_data.get('radiant_win'):
            radiant_wins += 1
        else:
            dire_wins += 1


        duration = match_data.get('duration', 0)
        total_duration += duration
        match_durations.append(duration)


        players = match_data.get('players', [])
        players_per_match.append(len(players))

    except Exception as e:
        print(f"❌ Ошибка чтения файла {filename}: {e}")


avg_duration_minutes = total_duration / len(match_files) / 60
avg_players = sum(players_per_match) / len(players_per_match)


shortest_match = min(match_durations) // 60
longest_match = max(match_durations) // 60

print(f"\n📈 ОСНОВНАЯ СТАТИСТИКА:")
print(f"   🏆 Побед Radiant: {radiant_wins} ({radiant_wins / len(match_files) * 100:.1f}%)")
print(f"   🏆 Побед Dire: {dire_wins} ({dire_wins / len(match_files) * 100:.1f}%)")
print(f"   ⏱️  Средняя длительность: {avg_duration_minutes:.1f} минут")
print(f"   🚀 Самый короткий матч: {shortest_match} минут")
print(f"   🐌 Самый длинный матч: {longest_match} минут")
print(f"   👥 Игроков в матче: {avg_players:.1f}")


print(f"\n🎮 АНАЛИЗ ГЕРОЕВ:")
print("   Подсчитываем популярных героев...")

hero_wins = {}
hero_picks = {}

for filename in match_files[:50]:  # Анализируем первые 50 матчей для скорости
    filepath = os.path.join(matches_folder, filename)

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            match_data = json.load(f)

        radiant_win = match_data.get('radiant_win')
        players = match_data.get('players', [])

        for player in players:
            hero_id = player.get('hero_id')
            if hero_id is None:
                continue


            if hero_id not in hero_picks:
                hero_picks[hero_id] = 0
            hero_picks[hero_id] += 1


            if hero_id not in hero_wins:
                hero_wins[hero_id] = 0

            is_radiant = player.get('isRadiant', False)
            if (is_radiant and radiant_win) or (not is_radiant and not radiant_win):
                hero_wins[hero_id] += 1

    except Exception as e:
        continue


if hero_picks:
    heroes_df = pd.read_csv('heroes.csv')
    hero_names = dict(zip(heroes_df['id'], heroes_df['name']))


    popular_heroes = sorted(hero_picks.items(), key=lambda x: x[1], reverse=True)[:10]

    print(f"\n🏆 ТОП-10 САМЫХ ПОПУЛЯРНЫХ ГЕРОЕВ:")
    for i, (hero_id, picks) in enumerate(popular_heroes, 1):
        wins = hero_wins.get(hero_id, 0)
        win_rate = (wins / picks) * 100 if picks > 0 else 0
        hero_name = hero_names.get(hero_id, f"Герой {hero_id}")

        print(f"   {i:2d}. {hero_name:20} - {picks:2d} пиков, {win_rate:.1f}% побед")

print(f"\n✅ АНАЛИЗ ЗАВЕРШЕН!")
print(f"📊 Проанализировано: {len(match_files)} матчей")
print(f"🎯 Теперь у нас есть данные для обучения модели!")

print(f"\n=== ГОТОВО К СЛЕДУЮЩЕМУ ШАГУ ===")
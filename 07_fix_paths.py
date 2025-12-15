import os
import shutil

print("=== НАСТРОЙКА ПУТЕЙ ФАЙЛОВ ===")

current_dir = os.getcwd()
print(f"Текущая папка: {current_dir}")

print("\n🔍 Ищем файлы проекта...")

files_found = {
    '01_test_api.py': False,
    '02_collect_heroes.py': False,
    '05_prepare_ml_data.py': False,
    'heroes.csv': False,
    'ml_data/X_features.csv': False
}

for root, dirs, files in os.walk('.'):
    for file in files:
        if file in files_found:
            full_path = os.path.join(root, file)
            files_found[file] = full_path
            print(f"✅ Найден: {full_path}")

print("\n📊 РЕЗУЛЬТАТ ПОИСКА:")
for file, path in files_found.items():
    if path:
        print(f"  {file}: ✅ найдено")
    else:
        print(f"  {file}: ❌ не найдено")

print("\n💡 РЕШЕНИЕ:")
if files_found['05_prepare_ml_data.py'] and files_found['heroes.csv']:
    print("1. Запусти 05_prepare_ml_data.py из той же папки где он лежит")
    print("2. После этого ml_data создастся в правильном месте")
else:
    print("Найди папку где лежат файлы 01_test_api.py, 02_collect_heroes.py и т.д.")
    print("Перейди в нее и запускай оттуда")

print("\nДля обучения модели нужно:")
print("1. Быть в папке с файлами проекта")
print("2. Иметь папку ml_data/ с файлами")
print("3. Запустить 06_train_model.py")
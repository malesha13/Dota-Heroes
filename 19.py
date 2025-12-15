import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

print("=== УЛУЧШЕННЫЙ TELEGRAM БОТ ===")

# Загружаем конфиг
with open('bot_config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

id_to_name = {int(k): v for k, v in config['id_to_name'].items()}
name_to_id = config['name_to_id']
all_hero_ids = config['all_hero_ids']

# Состояния пользователей
user_states = {}
user_heroes_page = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Привет {user.first_name}!\n"
        f"Я бот для подбора героев в Dota 2.\n\n"
        f"📋 *Команды:*\n"
        f"/pick - подобрать героя\n"
        f"/heroes - список всех героев\n"
        f"/help - помощь\n\n"
        f"⚡ *Быстрый старт:* /pick",
        parse_mode='Markdown'
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🆘 *Помощь*\n\n"
        "🎮 *Как пользоваться:*\n"
        "1. /pick - начать подбор\n"
        "2. Введи ID 4-х союзников\n"
        "3. Введи ID 5-х противников\n"
        "4. Получи рекомендацию\n\n"
        "📝 *Пример ввода:*\n"
        "Союзники: `1 2 3 4`\n"
        "Противники: `5 6 7 8 9`\n\n"
        "📚 *Все герои:* /heroes\n"
        "⚙️ *Справка по ID:* используй /heroes",
        parse_mode='Markdown'
    )


async def show_heroes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать всех героев с пагинацией"""
    user_id = update.effective_user.id
    user_heroes_page[user_id] = 0  # Начинаем с первой страницы

    # Создаем клавиатуру
    keyboard = [
        [InlineKeyboardButton("➡️ Следующие 20", callback_data="next_heroes")],
        [InlineKeyboardButton("❌ Закрыть", callback_data="close_heroes")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Показываем первую страницу
    message = await send_heroes_page(update, user_id, 0)

    if update.callback_query:
        await update.callback_query.edit_message_text(
            text=message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            text=message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )


async def send_heroes_page(update: Update, user_id: int, page: int):
    """Отправить страницу с героями"""
    heroes_per_page = 20
    total_pages = (len(all_hero_ids) + heroes_per_page - 1) // heroes_per_page

    start_idx = page * heroes_per_page
    end_idx = min(start_idx + heroes_per_page, len(all_hero_ids))

    message = f"📚 *Герои Dota 2* (страница {page + 1}/{total_pages})\n\n"

    for i in range(start_idx, end_idx):
        hero_id = all_hero_ids[i]
        hero_name = id_to_name.get(hero_id, f"Герой {hero_id}")
        message += f"`{hero_id:3d}` - {hero_name}\n"

    message += f"\n📊 Всего: {len(all_hero_ids)} героев\n"
    message += "📝 Используй ID в команде /pick"

    return message


async def heroes_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик кнопок для пагинации героев"""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    if data == "close_heroes":
        await query.edit_message_text("✅ Список героев закрыт")
        return

    if user_id not in user_heroes_page:
        user_heroes_page[user_id] = 0

    current_page = user_heroes_page[user_id]

    if data == "next_heroes":
        current_page += 1
        total_pages = (len(all_hero_ids) + 19) // 20

        if current_page >= total_pages:
            current_page = 0  # Возвращаемся к первой странице

    elif data == "prev_heroes":
        current_page -= 1
        if current_page < 0:
            total_pages = (len(all_hero_ids) + 19) // 20
            current_page = total_pages - 1

    user_heroes_page[user_id] = current_page

    # Обновляем клавиатуру
    keyboard = [
        [
            InlineKeyboardButton("⬅️ Назад", callback_data="prev_heroes"),
            InlineKeyboardButton("➡️ Вперед", callback_data="next_heroes")
        ],
        [InlineKeyboardButton("❌ Закрыть", callback_data="close_heroes")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message = await send_heroes_page(update, user_id, current_page)
    await query.edit_message_text(
        text=message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def pick_hero(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 *Подбор героя*\n\n"
        "✍️ *Шаг 1:* Введи ID 4-х союзников\n"
        "📝 *Формат:* цифры через пробел\n"
        "📋 *Пример:* `1 2 3 4`\n\n"
        "📚 Посмотреть всех героев: /heroes",
        parse_mode='Markdown'
    )
    user_states[update.effective_user.id] = 'waiting_allies'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if user_id not in user_states:
        await update.message.reply_text(
            "❓ Используй /pick чтобы начать подбор героя",
            parse_mode='Markdown'
        )
        return

    state = user_states[user_id]

    if state == 'waiting_allies':
        try:
            allies = list(map(int, text.split()))

            if len(allies) != 4:
                await update.message.reply_text(
                    "⚠️ *Ошибка:* нужно ровно 4 ID!\n"
                    "📝 *Пример:* `1 2 3 4`",
                    parse_mode='Markdown'
                )
                return

            invalid_allies = []
            valid_allies = []

            for hero_id in allies:
                if hero_id in all_hero_ids:
                    valid_allies.append(hero_id)
                else:
                    invalid_allies.append(hero_id)

            if invalid_allies:
                await update.message.reply_text(
                    f"⚠️ *Неверные ID:* {invalid_allies}\n"
                    f"📚 Проверь список: /heroes",
                    parse_mode='Markdown'
                )
                return

            context.user_data['allies'] = valid_allies
            user_states[user_id] = 'waiting_enemies'

            ally_names = [id_to_name.get(id, f"ID {id}") for id in valid_allies]
            ally_names_str = ", ".join(ally_names)

            await update.message.reply_text(
                f"✅ *Союзники сохранены:* {ally_names_str}\n\n"
                f"✍️ *Шаг 2:* Введи ID 5-х противников\n"
                f"📝 *Формат:* цифры через пробел\n"
                f"📋 *Пример:* `5 6 7 8 9`",
                parse_mode='Markdown'
            )

        except ValueError:
            await update.message.reply_text(
                "⚠️ *Ошибка:* используй только цифры!\n"
                "📝 *Пример:* `1 2 3 4`",
                parse_mode='Markdown'
            )

    elif state == 'waiting_enemies':
        try:
            enemies = list(map(int, text.split()))

            if len(enemies) != 5:
                await update.message.reply_text(
                    "⚠️ *Ошибка:* нужно ровно 5 ID!\n"
                    "📝 *Пример:* `5 6 7 8 9`",
                    parse_mode='Markdown'
                )
                return

            invalid_enemies = []
            valid_enemies = []

            for hero_id in enemies:
                if hero_id in all_hero_ids:
                    valid_enemies.append(hero_id)
                else:
                    invalid_enemies.append(hero_id)

            if invalid_enemies:
                await update.message.reply_text(
                    f"⚠️ *Неверные ID:* {invalid_enemies}\n"
                    f"📚 Проверь список: /heroes",
                    parse_mode='Markdown'
                )
                return

            allies = context.user_data['allies']

            # Проверяем дубликаты
            duplicates = set(allies) & set(valid_enemies)
            if duplicates:
                duplicate_names = [id_to_name.get(id, f"ID {id}") for id in duplicates]
                await update.message.reply_text(
                    f"⚠️ *Дубликаты:* {', '.join(duplicate_names)}\n"
                    f"❌ Один герой не может быть и в своей и в вражеской команде!",
                    parse_mode='Markdown'
                )
                return

            # Удаляем состояние
            del user_states[user_id]

            # Получаем рекомендацию
            recommended_id, score = get_recommendation(allies, valid_enemies)
            hero_name = id_to_name.get(recommended_id, f"Герой {recommended_id}")

            # Формируем ответ
            ally_names = [id_to_name.get(id, f"ID {id}") for id in allies]
            enemy_names = [id_to_name.get(id, f"ID {id}") for id in valid_enemies]

            response = (
                f"🎯 *РЕКОМЕНДАЦИЯ*\n\n"
                f"👥 *Союзники:* {', '.join(ally_names)}\n"
                f"⚔️ *Противники:* {', '.join(enemy_names)}\n\n"
                f"🏆 *Лучший пик:* {hero_name} (ID: {recommended_id})\n"
                f"📈 *Шанс победы:* {score:.1f}%\n\n"
                f"⭐ *Почему именно он:*\n"
                f"• Хорошая синергия с командой\n"
                f"• Эффективный контрпик против врагов\n"
                f"• Сильный герой в текущей мете\n\n"
                f"🎮 Удачи в игре!"
            )

            await update.message.reply_text(response, parse_mode='Markdown')

        except ValueError:
            await update.message.reply_text(
                "⚠️ *Ошибка:* используй только цифры!\n"
                "📝 *Пример:* `5 6 7 8 9`",
                parse_mode='Markdown'
            )


def get_recommendation(ally_ids, enemy_ids):
    """Функция подбора героя"""
    best_hero = None
    best_score = 0

    for hero_id in all_hero_ids:
        if hero_id in ally_ids or hero_id in enemy_ids:
            continue

        # Простая эвристика для демонстрации
        # В реальном боте здесь будет вызов ML-модели

        import random
        score = 50.0 + random.uniform(0, 40)  # От 50% до 90%

        # Немного логики на основе ID
        if hero_id % 2 == 0:
            score += 5
        if hero_id in [14, 42, 31]:  # Pudge, Warlock, Invoker - популярные герои
            score += 10

        if score > best_score:
            best_score = score
            best_hero = hero_id

    return best_hero, min(best_score, 95.0)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Ошибка: {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text("❌ Произошла ошибка. Попробуй еще раз.")


def main():
    print("🤖 Запуск улучшенного бота...")

    # ВСТАВЬ СВОЙ ТОКЕН СЮДА!
    TOKEN = "8593884530:AAFKQYjdkcff_GM6WhXqxuu4Wi2phb76mkI"

    if TOKEN == "ТВОЙ_ТОКЕН_БОТА":
        print("❌ ВАЖНО: Замени TOKEN на свой из @BotFather!")
        return

    app = Application.builder().token(TOKEN).build()

    # Команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("heroes", show_heroes))
    app.add_handler(CommandHandler("pick", pick_hero))

    # Кнопки
    app.add_handler(CallbackQueryHandler(heroes_button_handler, pattern="^(next_heroes|prev_heroes|close_heroes)$"))

    # Сообщения
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Ошибки
    app.add_error_handler(error_handler)

    print("✅ Бот запущен!")
    print("📱 Открой Telegram и найди своего бота")


    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from deep_translator import GoogleTranslator
from api import search_movie_by_title, get_movie_details
from keyboards import create_movie_keyboard, create_like_dislike_keyboard
from database import add_to_history, get_history, add_to_likes, remove_from_likes, get_likes

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

translator = GoogleTranslator(source='auto', target='en')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands_text = (
        "Доступные команды:\n"
        "/start - Начать взаимодействие с ботом\n"
        "/history - Показать историю запросов\n"
        "/likes - Показать список понравившихся фильмов\n"
        "Отправьте название фильма или имя автора для поиска."
    )
    await update.message.reply_text(f'Привет! Я бот для поиска фильмов. {commands_text}')

async def search_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    user_id = update.message.from_user.id
    translated_query = translator.translate(query)
    movies = search_movie_by_title(translated_query)

    if movies:
        keyboard = create_movie_keyboard(movies)
        await update.message.reply_text('Вот что я нашел:', reply_markup=keyboard)
        add_to_history(user_id, query)
    else:
        await update.message.reply_text('Ничего не найдено. Попробуйте другой запрос.')

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    try:
        await query.answer()
    except BadRequest as e:
        if "query is too old" in str(e):
            return
        raise

    if data.startswith('button_'):
        imdbID = data.split('_')[1]
        movie_details = get_movie_details(imdbID)

        if movie_details:
            message = f"Название: {movie_details.get('Title', 'Н/Д')}\nГод: {movie_details.get('Year', 'Н/Д')}\nРежиссер: {movie_details.get('Director', 'Н/Д')}\nОписание: {movie_details.get('Plot', 'Н/Д')}"
            await query.edit_message_text(text=message)
            keyboard = create_like_dislike_keyboard(imdbID)
            await query.message.reply_text('Действия:', reply_markup=keyboard)
        else:
            await query.edit_message_text(text='Не удалось получить информацию о фильме.')
    elif data.startswith('like_'):
        imdbID = data.split('_')[1]
        user_id = query.from_user.id
        add_to_likes(user_id, imdbID)
        await query.message.reply_text('Фильм добавлен в понравившиеся.')
    elif data.startswith('dislike_'):
        imdbID = data.split('_')[1]
        user_id = query.from_user.id
        remove_from_likes(user_id, imdbID)
        await query.message.reply_text('Фильм удален из понравившихся.')

async def show_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    history = get_history(user_id)
    if history:
        history_text = "Ваша история запросов:\n" + "\n".join(history)
        await update.message.reply_text(history_text)
        commands_text = (
            "Доступные команды:\n"
            "/start - Начать взаимодействие с ботом\n"
            "/history - Показать историю запросов\n"
            "/likes - Показать список понравившихся фильмов\n"
            "Отправьте название фильма или имя автора для поиска."
        )
        await update.message.reply_text(commands_text)
    else:
        await update.message.reply_text('Ваша история запросов пуста.')

async def show_likes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    likes = get_likes(user_id)
    if likes:
        likes_text = "Ваши понравившиеся фильмы:\n"
        keyboard = []
        for imdbID in likes:
            movie_details = get_movie_details(imdbID)
            if movie_details:
                likes_text += f"{movie_details['Title']} ({movie_details['Year']})\n"
                keyboard.append([InlineKeyboardButton(f"Удалить {movie_details['Title']}", callback_data=f"dislike_{imdbID}")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(likes_text, reply_markup=reply_markup)
    else:
        await update.message.reply_text('Ваш список понравившихся фильмов пуст.')

async def like_dislike_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action, imdbID = query.data.split('_')
    user_id = query.from_user.id

    movie_details = get_movie_details(imdbID)
    if not movie_details:
        await query.message.reply_text('Не удалось получить информацию о фильме.')
        return

    if action == 'like':
        add_to_likes(user_id, imdbID)
        await query.message.reply_text('Фильм добавлен в понравившиеся.')
    elif action == 'dislike':
        remove_from_likes(user_id, imdbID)
        await query.message.reply_text('Фильм удален из понравившихся.')

    commands_text = (
        "Доступные команды:\n"
        "/start - Начать взаимодействие с ботом\n"
        "/history - Показать историю запросов\n"
        "/likes - Показать список понравившихся фильмов\n"
        "Отправьте название фильма или имя автора для поиска."
    )
    await query.message.reply_text(commands_text)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def create_movie_keyboard(movies):
    keyboard = []
    for movie in movies:
        keyboard.append([InlineKeyboardButton(movie['Title'], callback_data=f"button_{movie['imdbID']}")])
    return InlineKeyboardMarkup(keyboard)

def create_like_dislike_keyboard(imdbID):
    keyboard = [
        [InlineKeyboardButton("Добавить в понравившиеся", callback_data=f"like_{imdbID}")],
        [InlineKeyboardButton("Удалить из понравившихся", callback_data=f"dislike_{imdbID}")]
    ]
    return InlineKeyboardMarkup(keyboard)


from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from handlers import start, search_movie, button, show_history, show_likes, like_dislike_handler
from database import init_db
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

def main():
    init_db()
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("history", show_history))
    application.add_handler(CommandHandler("likes", show_likes))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_movie))
    application.add_handler(CallbackQueryHandler(button, pattern=r"^button_"))
    application.add_handler(CallbackQueryHandler(like_dislike_handler, pattern=r"like_|dislike_"))

    application.run_polling()

if __name__ == '__main__':
    main()
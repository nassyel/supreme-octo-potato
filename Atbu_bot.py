import os
import sqlite3
from telegram import Update
from telegram.ext import Updater, CommandHandler

db_path = os.path.join(os.getcwd(), "atbu_notes.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        course_code TEXT PRIMARY KEY,
        drive_link TEXT
    )
""")
conn.commit()

def start(update: Update, context):
    update.message.reply_text("📚 ATBU Notes Bot: Use /search COURSE_CODE")

def search_notes(update: Update, context):
    course_code = update.message.text.replace("/search", "").strip().upper()
    cursor.execute("SELECT drive_link FROM notes WHERE course_code = ?", (course_code,))
    result = cursor.fetchone()
    if result:
        update.message.reply_text(f"📚 {course_code}:\n{result[0]}")
    else:
        update.message.reply_text("❌ Not found. Use /request to ask for it.")

TOKEN = os.environ.get("TOKEN")
updater = Updater(TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler("search", search_notes))

print("Bot is running...")
updater.start_polling()
updater.idle()

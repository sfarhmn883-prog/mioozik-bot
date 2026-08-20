import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎵 هلا بيك!\n"
        "أنا بوت ميوزك العراقي 🇮🇶\n\n"
        "اكتب /help حتى تشوف الأوامر."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎧 أوامر البوت:\n"
        "/start - تشغيل البوت\n"
        "/help - المساعدة\n"
        "/play - تشغيل الموسيقى (قريباً)"
    )

def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN غير موجود")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    print("🎵 Music Bot Started")
    app.run_polling()

if __name__ == "__main__":
    main()
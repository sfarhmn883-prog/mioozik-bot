import os
import tempfile
import yt_dlp

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎵 هلا بيك!\n\n"
        "🇮🇶 أنا بوت الموسيقى العراقي\n\n"
        "اكتب:\n"
        "/help - أوامر البوت\n"
        "/play اسم الأغنية - تحميل الأغنية"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎧 أوامر البوت:\n\n"
        "/start - تشغيل البوت\n"
        "/help - المساعدة\n"
        "/play اسم الأغنية - تحميل الأغنية"
    )


async def play_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "❌ اكتب اسم الأغنية بعد الأمر.\n\n"
            "مثال:\n"
            "/play حسين الجسمي بشرة خير"
        )
        return

    query = " ".join(context.args)

    await update.message.reply_text(
        f"🔎 دا أبحث عن:\n{query}\n\n"
        "⏳ انتظر شوي..."
    )

    temp_dir = tempfile.mkdtemp()

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(temp_dir, "%(title)s.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                f"ytsearch1:{query}",
                download=True
            )

            if not info.get("entries"):
                await update.message.reply_text(
                    "❌ ما لكيت الأغنية."
                )
                return

            video = info["entries"][0]
            title = video.get("title", "الأغنية")

            file_path = ydl.prepare_filename(video)

        await update.message.reply_audio(
            audio=open(file_path, "rb"),
            title=title,
            performer=video.get("uploader"),
        )

    except Exception as e:
        print("ERROR:", e)
        await update.message.reply_text(
            "❌ صار خطأ أثناء تحميل الأغنية."
        )


def main():
    if not TOKEN:
        raise RuntimeError(
            "BOT_TOKEN غير موجود. أضفه في Environment Variables."
        )

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("play", play_command))

    print("🎵 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
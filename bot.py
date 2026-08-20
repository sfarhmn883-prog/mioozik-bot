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
        "/help - الأوامر\n"
        "/play اسم الأغنية - تحميل الأغنية"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎧 أوامر البوت:\n\n"
        "/start - تشغيل البوت\n"
        "/help - المساعدة\n"
        "/play اسم الأغنية - تشغيل وتحميل الأغنية"
    )


async def play_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "🎵 اكتب اسم الأغنية بعد الأمر.\n\n"
            "مثال:\n"
            "/play كاظم الساهر زيديني عشقاً"
        )
        return

    query = " ".join(context.args)

    msg = await update.message.reply_text(
        f"🔎 أبحث عن:\n{query}\n\n⏳ انتظر..."
    )

    temp_dir = tempfile.mkdtemp()

    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(temp_dir, "%(title)s.%(ext)s"),
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                f"ytsearch1:{query}",
                download=True
            )

            if "entries" in info:
                info = info["entries"][0]

            file_path = ydl.prepare_filename(info)
            title = info.get("title", query)

        await msg.edit_text(
            f"✅ لقيتها:\n{title}\n\n📤 جاري الإرسال..."
        )

        with open(file_path, "rb") as audio:
            await update.message.reply_audio(
                audio=audio,
                title=title[:64],
                performer="Mioozik Bot"
            )

        await msg.delete()

    except Exception as e:
        print("ERROR:", e)

        await msg.edit_text(
            "❌ صار خطأ أثناء تحميل الأغنية.\n"
            "جرّب اسم أغنية ثاني."
        )

    finally:
        try:
            for file in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, file))
            os.rmdir(temp_dir)
        except Exception:
            pass


def main():
    if not TOKEN:
        raise RuntimeError(
            "BOT_TOKEN غير موجود"
        )

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("help", help_command)
    )

    app.add_handler(
        CommandHandler("play", play_command)
    )

    print("🎵 Music Bot Started!")

    app.run_polling()


if __name__ == "__main__":
    main()
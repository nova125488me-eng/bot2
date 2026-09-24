import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)
import asyncio

# بارگذاری متغیرهای محیطی
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"سلام {update.effective_user.first_name}!\n"
        "من ربات نمونه‌ی تو هستم. از /help برای راهنما استفاده کن."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "/start - شروع\n"
        "/help - راهنما\n"
        "/echo <متن> - متن رو بازتاب بده"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = " ".join(context.args)
    await update.message.reply_text(text if text else "هیچ متنی وارد نکردی!")

async def main() -> None:
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("echo", echo))

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())

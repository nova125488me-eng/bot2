import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define states
ASK_NAME, ASK_AGE = range(2)

def start(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'سلام {user.mention_markdown_v2()}\! من یک ربات ساده هستم\.\n'
        r'لطفاً نام خود را بنویسید\.',
        reply_markup=ForceReply(selective=True),
    )
    return ASK_NAME

def ask_name(update: Update, context: CallbackContext) -> int:
    context.user_data['name'] = update.message.text
    update.message.reply_text(
        f'خوبه، {context.user_data["name"]}! حالا چند سال سن داری؟'
    )
    return ASK_AGE

def ask_age(update: Update, context: CallbackContext) -> int:
    try:
        age = int(update.message.text)
    except ValueError:
        update.message.reply_text(
            'لطفاً یک عدد وارد کن. 😅'
        )
        return ASK_AGE
    context.user_data['age'] = age
    update.message.reply_text(
        f'کافی عالی! تو {age} ساله‌ای. همین حالا می‌تونیم شروع کنیم.\n'
        'برای اطلاعات بیشتر از /help استفاده کن.'
    )
    return ConversationHandler.END

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'این یک ربات نمونه است.\n'
        'استفاده از دستورات:\n'
        '/start - شروع\n'
        '/help - راهنما\n'
        '/echo <متن> - بازتاب متن'
    )

def echo(update: Update, context: CallbackContext) -> None:
    if context.args:
        update.message.reply_text(' '.join(context.args))
    else:
        update.message.reply_text('لطفاً چیزی برای بازتاب بنویسید.')

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('رابطه‌مون تمام شد. خداحافظ! 👋')
    return ConversationHandler.END

def main() -> None:
    updater = Updater("YOUR_BOT_TOKEN")
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ASK_NAME: [MessageHandler(Filters.text & ~Filters.command, ask_name)],
            ASK_AGE: [MessageHandler(Filters.text & ~Filters.command, ask_age)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('echo', echo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

# Additional utilities
def dummy_function():
    """A dummy function that does nothing."""
    pass

def another_dummy():
    # Just another placeholder
    return None

# End of file
# Keep the bot alive with a simple ping
print("Bot module loaded su

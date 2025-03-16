from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

ADMIN_CHAT_ID = 0
AWAITING_TEXT, AWAITING_PICTURE, CHOICE, GAMES, RATE, AWAITING_ID, AWAITING_MESSAGE = range(7)
USER_ID = 0


async def reply_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id == ADMIN_CHAT_ID:
        await update.message.reply_text(f"Введи айдишник пользователя\U00002764(Текущий айди: {USER_ID}):")
        return AWAITING_ID
    else:
        return ConversationHandler.END


async def id_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global USER_ID
    USER_ID = update.message.text
    await update.message.reply_text("Введи сообщение для пользователя:")
    return AWAITING_MESSAGE

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    await context.bot.send_message(USER_ID, message_text)
    return ConversationHandler.END
async def reply_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id == ADMIN_CHAT_ID:
        await update.message.reply_text('Начинаем ответ!')
        await update.message.reply_text('Укажи id пользователя:')
        return AWAITING_ID
    else:
        return ConversationHandler.END


async def waiting_for_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global USER_ID
    text = update.message.text
    USER_ID = text
    await update.message.reply_text('Укажи сообщение для пользователя:')
    return AWAITING_REPLY_TEXT

async def reply_command_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id == ADMIN_CHAT_ID:
        await update.message.reply_text('Начинаем ответ!')
        await update.message.reply_text('Укажи id пользователя:')
        return AWAITING_ID
    else:
        return ConversationHandler.END


async def waiting_for_id_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global USER_ID
    text = update.message.text
    USER_ID = text
    await update.message.reply_text('Укажи сообщение для пользователя:')
    return AWAITING_REPLY_PHOTO


async def awaiting_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    print(text)
    print(USER_ID)
    await context.bot.send_message(chat_id=USER_ID, text=text)
    return ConversationHandler.END


async def awaiting_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    print(text)
    print(USER_ID)
    await context.bot.send_message(chat_id=USER_ID, text=text)
    return ConversationHandler.END
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

AWAITING_TEXT, AWAITING_PICTURE, CHOICE, GAMES, RATE, AWAITING_ID, AWAITING_MESSAGE = range(7)
STATE_ZERO = -1
ADMIN_CHAT_ID = 0
EXCHANGE_RATE = 0.61
MY_PERCENT = 1.20

async def exchange_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id == ADMIN_CHAT_ID:
        await update.message.reply_text('Введите новый курс обмена йена - рубль:')
        return RATE
    else:
        return ConversationHandler.END

async def set_exchange_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global EXCHANGE_RATE
    EXCHANGE_RATE = update.message.text
    EXCHANGE_RATE = float(EXCHANGE_RATE.strip())
    return ConversationHandler.END

async def catalog_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['state'] = CHOICE
    button1 = KeyboardButton('Карты пополнения')
    button2 = KeyboardButton('Коды на игры')
    reply_markup = ReplyKeyboardMarkup([[button1, button2]], resize_keyboard=True)
    await update.message.reply_text('Цены на что вас интересуют?', reply_markup=reply_markup)
    return CHOICE


async def games_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_id = update.message.message_id
    if update.message.text:
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Пользователь {update.message.chat_id} поитересовался ценой:")
        await context.bot.forward_message(chat_id=ADMIN_CHAT_ID, from_chat_id=update.message.chat_id, message_id=message_id)
        await update.message.reply_text('Благодарим за обращение! Наша команда ответит вам в ближайшее время.')
        context.user_data['state'] = STATE_ZERO
        return ConversationHandler.END
    else:
        await update.message.reply_text("Пожалуйста, используйте *текст*, иначе мы не сможем Вас понять!", parse_mode=ParseMode.MARKDOWN)

async def choice_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    selected_option = update.message.text
    if selected_option == 'Карты пополнения':
        await update.message.reply_text('Загружаю каталог...')
        exchange_rate_percents = EXCHANGE_RATE * MY_PERCENT
        await update.message.reply_text('Текущие цены:\n'
                                        '\U0001F1EF\U0001F1F5 Карты пополения Eshop\n'
                                        f'1000JPY: {int(exchange_rate_percents * 1000)}RUB\n'
                                        f'3000JPY: {int(exchange_rate_percents * 3000)}RUB\n'
                                        f'5000JPY: {int(exchange_rate_percents * 5000)}RUB\n'
                                        f'9000JPY: {int(exchange_rate_percents * 9000)}RUB\n',
                                        reply_markup=ReplyKeyboardRemove())
        context.user_data['state'] = STATE_ZERO
        return ConversationHandler.END
    elif selected_option == 'Коды на игры':
        await update.message.reply_text("Следующим сообщением укажите, какие игры вас интересуют(например, Super Mario Bros. Wonder + Metroid Dread)" ,  reply_markup=ReplyKeyboardRemove())
        return GAMES
    elif selected_option != 'Коды на игры' and selected_option != 'Карты пополнения':
        await update.message.reply_text('Вернитесь к каталогу с помощью соответствующей команды /catalog',  reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END

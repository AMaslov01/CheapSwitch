from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

AWAITING_TEXT, AWAITING_PICTURE, CHOICE, GAMES, RATE, AWAITING_ID, AWAITING_MESSAGE = range(7)
ADMIN_CHAT_ID = 0

async def pay_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_state = context.user_data.get('state')
    if current_state == CHOICE:
        return
    await update.message.reply_text('Пожалуйста, уточните позиции, которые Вас интересуют, *текстом* в одно сообщение(например, 1000JPY + 5000JPY):\n'
                                    'Для отмены процедуры оплаты нажмите сюда \U0001F449 /cancel', parse_mode=ParseMode.MARKDOWN)
    return AWAITING_TEXT


async def waiting_for_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_id = update.message.message_id
    if update.message.text:
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Пользователь {update.message.chat_id} указал товар:")
        await context.bot.forward_message(chat_id=ADMIN_CHAT_ID, from_chat_id=update.message.chat_id, message_id=message_id)
        await update.message.reply_text('\U0001F4B3Реквизиты для оплаты:\n'
                                        'Сбербанк: 4276 5501 0150 4093 Артемий Игоревич М.\n'
                                        'Тинькофф: 2200 7008 9680 9521 Артемий Игоревич М.\n'
                                        'Убедитесь, что на Вашем аккаунте установлен японский регион, в противном случае коды не сработают.\n'
                                        'После оплаты, пожалуйста, пришлите скриншот чека из банковского приложения *картинкой* прямо сюда.\n'
                                        'Для отмены процедуры оплаты нажмите сюда \U0001F449 /cancel', parse_mode=ParseMode.MARKDOWN)
        return AWAITING_PICTURE
    else:
        await update.message.reply_text("Пожалуйста, используйте *текст*, иначе мы не сможем Вас понять!"
                                        'Для отмены процедуры оплаты нажмите сюда \U0001F449 /cancel',
                                        parse_mode=ParseMode.MARKDOWN
                                        )


async def waiting_for_picture(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message_id = update.message.message_id
    if update.message.photo:
        await update.message.reply_text('Благодарим за покупку! Ожидайте подтверждения заказа и получение чека. \n'
                                        'Просим обратить внимание, что получение кода может занимать до двух часов в рабочее время.\n'
                                        'В случае получения оплаты в нерабочее время, заказ будет выполнен на следующий рабочий день.')
        await context.bot.send_message(chat_id=6424364197, text=f"Пользователь {update.message.chat_id} отправил чек об оплате:")
        await context.bot.forward_message(chat_id=6424364197, from_chat_id=update.message.chat_id, message_id=message_id)
        return ConversationHandler.END
    else:
        await update.message.reply_text("Пожалуйста, отправьте *фото*, иначе мы не сможем Вас понять!"
                                        'Для отмены процедуры оплаты нажмите сюда \U0001F449 /cancel',
                                        parse_mode=ParseMode.MARKDOWN
                                        )
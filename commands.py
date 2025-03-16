import logging

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

ADMIN_CHAT_ID = 0

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Оплата отменена! Для возобновления воспользуйтесь командой /pay.')
    await context.bot.send_message(ADMIN_CHAT_ID, f'Пользователь {update.message.chat_id} отменил оплату')
    return ConversationHandler.END

async def cancel_catalog_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Запрос отменен! Для возобновления воспользуйтесь командой /catalog.')
    return ConversationHandler.END
async def support_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('По любым вопросам пишите в поддержку: @cheapswitchsupport')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Список команд:\n'
                                    '/start - Начало диалога\n'
                                    '/pay - Оплата заказа\n'
                                    '/catalog - Каталог товаров\n'
                                    '/support - Поддержка\n'
                                    '/help - Список команд\n')


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.full_name
    logging.info(f'Logged: {username}')
    await update.message.reply_text(f'Здравствуйте, {username}! С помощью этого бота можно приобрести японские карты пополнения, а так же коды на цифровые версии игр для Nintendo Switch.\n\n'
                                    f'*Рабочее время:* Пн-Вс 09:00-21:00 по московскому времени', parse_mode=ParseMode.MARKDOWN)

from commands import *
from pay import *
from catalog import *
from reply import *


from telegram.ext import ApplicationBuilder, CommandHandler
from telegram.ext import filters, MessageHandler, ConversationHandler



AWAITING_TEXT, AWAITING_PICTURE, CHOICE, GAMES, RATE, AWAITING_ID, AWAITING_MESSAGE = range(7)


TOKEN = 'default'
ADMIN_CHAT_ID = 0
USER_ID = 0
FLAG = "AAA"
BUTTON = 100
#Commands




#MAIN:
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).arbitrary_callback_data(True).build()
    app.add_handler(CommandHandler('start', start_command), group=1)
    app.add_handler(CommandHandler('support', support_command), group=1)
    app.add_handler(CommandHandler('help', help_command), group=1)
    conversation_handler_pay = ConversationHandler(
        entry_points=[CommandHandler('pay', pay_command)],
        states={
            AWAITING_TEXT: [MessageHandler(filters.ALL & ~filters.Regex(r'^/cancel$'), waiting_for_text)],
            AWAITING_PICTURE: [MessageHandler(filters.ALL & ~filters.Regex(r'^/cancel$'), waiting_for_picture)]
        },
        fallbacks=[CommandHandler('cancel', cancel_command)]
    )
    conversation_handler_catalog = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex(r'^/catalog$'), catalog_command)],
        states={
            CHOICE: [MessageHandler(filters.ALL, choice_command)],
            GAMES: [MessageHandler(filters.ALL & ~filters.Regex(r'^/cancel$') &
                                   ~filters.Regex(r'^/pay$') & ~filters.Regex(r'^/catalog$'), games_command)]
        },
        fallbacks=[CommandHandler('cancel', cancel_catalog_command)]
    )
    conversation_handler_exchange = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex(r'^/exchange$'), exchange_command)],
        states={
            RATE: [MessageHandler(filters.ALL & ~filters.Regex(r'^/cancel$'), set_exchange_command)],
        },
        fallbacks=[CommandHandler('cancel', cancel_command)]
    )
    conversation_handler_reply = ConversationHandler(
        entry_points=[CommandHandler('reply', reply_command)],
        states={
            AWAITING_ID: [MessageHandler(filters.TEXT, id_handler)],
            AWAITING_MESSAGE: [MessageHandler(filters.ALL, message_handler)]
        },
        fallbacks=[CommandHandler('cancel', cancel_command)]
    )
    app.add_handler(conversation_handler_pay)
    app.add_handler(conversation_handler_catalog)
    app.add_handler(conversation_handler_exchange)
    app.add_handler(conversation_handler_reply)
    app.run_polling(0)

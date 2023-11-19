import telegram
from telegram.ext import Updater, MessageHandler, Filters

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
updater = Updater(token='6780752261:AAGH5NiObh6bUCzbniQ61q0XmafQVDNQRqI', use_context=True)
dispatcher = updater.dispatcher

def echo(update, context):
    chat_id = update.effective_chat.id
    message_text = update.message.text

    # Reply with the same message
    context.bot.send_message(chat_id=chat_id, text=message_text)

# Register the handler
echo_handler = MessageHandler(Filters.text & ~Filters.command, echo)
dispatcher.add_handler(echo_handler)

# Start the bot
updater.start_polling()
updater.idle()

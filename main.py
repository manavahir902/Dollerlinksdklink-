import telegram
from telegram.ext import Updater, MessageHandler, Filters
import pyshorteners

# Replace '6780752261:AAGH5NiObh6bUCzbniQ61q0XmafQVDNQRqI' with your actual bot token
updater = Updater(token='6780752261:AAGH5NiObh6bUCzbniQ61q0XmafQVDNQRqI', use_context=True)
dispatcher = updater.dispatcher

def shorten_links(update, context):
    chat_id = update.effective_chat.id
    message_text = update.message.text
    shortener = pyshorteners.Shortener()

    # Replace links in the message with shortened links
    shortened_message = ' '.join(shortener.short(link) if link.startswith('http') else link for link in message_text.split())

    # Send the updated message
    context.bot.send_message(chat_id=chat_id, text=shortened_message)

# Register the handler
link_handler = MessageHandler(Filters.text & ~Filters.command, shorten_links)
dispatcher.add_handler(link_handler)

# Start the bot
updater.start_polling()
updater.idle()

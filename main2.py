import telegram
from telegram.ext import Updater, CommandHandler
import requests
from bs4 import BeautifulSoup

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
updater = Updater(token='6780752261:AAGH5NiObh6bUCzbniQ61q0XmafQVDNQRqI', use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    chat_id = update.effective_chat.id

    # Check if a link is provided in the command
    if context.args:
        url = context.args[0]

        # Fetch the content of the provided link
        try:
            response = requests.get(url)
            response.raise_for_status()

            # Parse HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.get_text()

            # Send the content as a message
            context.bot.send_message(chat_id=chat_id, text=content)
        except Exception as e:
            context.bot.send_message(chat_id=chat_id, text=f"Error: {str(e)}")
    else:
        context.bot.send_message(chat_id=chat_id, text="Please provide a link.")

# Register the start command handler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Start the bot
updater.start_polling()
updater.idle()

import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import requests

# Replace '6780752261:AAGH5NiObh6bUCzbniQ61q0XmafQVDNQRqI' with your actual bot token
updater = Updater(token='6780752261:AAGH5NiObh6bUCzbniQ61q0XmafQVDNQRqI', use_context=True)
dispatcher = updater.dispatcher

def shorten_link(url):
    # Replace 'YOUR_API_KEY' with your actual API key from dollerlinksd.in
    api_key = '88c17813e37e9c8aadec0deb2ee997b544c34196'
    api_url = f'https://dollerlinksd.in/api?api={api_key}&url={url}'

    response = requests.get(api_url)
    if response.status_code == 200:
        return response.text
    else:
        return None

def start(update, context):
    chat_id = update.effective_chat.id

    # Send a welcome message
    context.bot.send_message(chat_id=chat_id, text="Hello! I'm your link shortening bot. Send me a link, and I'll shorten it for you.")

# Register the start command handler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def handle_links(update, context):
    chat_id = update.effective_chat.id
    message_text = update.message.text

    # Check if the message contains a link
    if 'http' in message_text:
        # Shorten the link using dollerlinksd.in
        shortened_link = shorten_link(message_text)

        if shortened_link:
            # Reply with the shortened link
            context.bot.send_message(chat_id=chat_id, text=f"Shortened link: {shortened_link}")
        else:
            # Handle error if link shortening fails
            context.bot.send_message(chat_id=chat_id, text="Failed to shorten the link. Please try again.")
    else:
        # Reply with a default response if no link is found
        context.bot.send_message(chat_id=chat_id, text="Hello! If you send a link, I'll try to shorten it for you.")

# Register the link handler
link_handler = MessageHandler(Filters.text & ~Filters.command, handle_links)
dispatcher.add_handler(link_handler)

# Start the bot
updater.start_polling()
updater.idle()

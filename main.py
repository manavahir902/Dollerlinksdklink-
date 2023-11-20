import telegram
from telegram.ext import Updater, MessageHandler, Filters
import requests

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
updater = Updater(token='6780752261:AAGH5NiObh6bUCzbniQ61q0XmafQVDNQRqI', use_context=True)
dispatcher = updater.dispatcher

def shorten_link(url):
    # Replace 'YOUR_API_KEY' with your actual API key from dollerlinksd.in
    api_key = 'fd1a97fe23c350f2d1ae48b40d6d91313dd89eee'
    api_url = f'https://adsfly.in/api?api={api_key}&url={url}'

    response = requests.get(api_url)
    if response.status_code == 200:
        return response.text
    else:
        return None

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

# Register the handler
link_handler = MessageHandler(Filters.text & ~Filters.command, handle_links)
dispatcher.add_handler(link_handler)

# Start the bot
updater.start_polling()
updater.idle()

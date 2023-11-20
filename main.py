
import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import requests
import time

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
updater = Updater(token='6780752261:AAGH5NiObh6bUCzbniQ61q0XmafQVDNQRqI', use_context=True)
dispatcher = updater.dispatcher

# Replace 'YOUR_API_KEY' with your actual API key from adsfly.in
API_KEY = 'fd1a97fe23c350f2d1ae48b40d6d91313dd89eee'

# Add a delay (in seconds) before each request to Adsfly.in
REQUEST_DELAY = 5

def shorten_link(url):
    api_url = f'https://adsfly.in/api'
    params = {
        'api': API_KEY,
        'url': url
    }

    try:
        # Introduce a delay before the request
        time.sleep(REQUEST_DELAY)

        response = requests.post(api_url, params=params)
        response.raise_for_status()

        # Include the entire API response in the shortened_url variable
        shortened_url = response.text

        return shortened_url
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
        return None
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
        return None
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
        return None
    except requests.exceptions.RequestException as err:
        print("Something went wrong:", err)
        return None


def start(update, context):
    chat_id = update.effective_chat.id

    # Send a welcome message
    context.bot.send_message(chat_id=chat_id, text="Hello! I'm your link shortening bot. Send me a link, and I'll shorten it for you.")
    context.bot.send_message(chat_id=chat_id, text=f" {API_KEY} Hello! I'm your link shortening bot. Send me a link, and I'll shorten it for you.")


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



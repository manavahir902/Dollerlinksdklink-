import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import requests
import time

# Replace '6780752261:AAGH5NiObh6bUCzbniQ61q0XmafQVDNQRqI' with your actual bot token
updater = Updater(token='6780752261:AAGH5NiObh6bUCzbniQ61q0XmafQVDNQRqI', use_context=True)
dispatcher = updater.dispatcher

# Replace 'YOUR_API_KEY' with your actual API key from dollerlinksd.in
API_KEY = '88c17813e37e9c8aadec0deb2ee997b544c34196'

def shorten_link(url):
    api_url = f'https://dollerlinksd.in/api?api={API_KEY}&url={url}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Parse JSON response and extract the shortened URL
        shortened_url = response.json().get('shortenedUrl', '')

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

# Rest of the code remains unchanged...

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


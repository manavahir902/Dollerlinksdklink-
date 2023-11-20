
import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import requests
import time
import http.client
import urllib.request
import urllib.parse

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
updater = Updater(token='6780752261:AAGH5NiObh6bUCzbniQ61q0XmafQVDNQRqI', use_context=True)
dispatcher = updater.dispatcher

# Replace 'YOUR_API_KEY' with your actual API key from adsfly.in
API_KEY = 'fd1a97fe23c350f2d1ae48b40d6d91313dd89eee'

# Add a delay (in seconds) before each request to Adsfly.in
REQUEST_DELAY = 5

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}




def shorten_link(url):
    api_url = f'https://adsfly.in/api?api={API_KEY}&url={urllib.parse.quote(url)}'

    try:
        # Introduce a delay before the request
        time.sleep(REQUEST_DELAY)

        # Parse the URL to get host and path
        parsed_url = urllib.parse.urlparse(api_url)
        connection = http.client.HTTPSConnection(parsed_url.netloc)

        # Send a GET request
        connection.request("GET", parsed_url.path + '?' + parsed_url.query)

        # Get the response
        response = connection.getresponse()

        if response.status == 200:
            # Parse JSON response and extract the shortened URL
            shortened_url = response.read().decode('utf-8')
            return shortened_url
        else:
            print(f"HTTP Error: {response.status}")
            return None
    except Exception as e:
        print(f"Something went wrong: {e}")
        return None

# Rest of the code remains unchanged...






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




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
    api_url = f'https://adsfly.in/api?api={API_KEY}&url={url}'

    try:
        # Introduce a delay before the request
        time.sleep(REQUEST_DELAY)

        response = requests.get(api_url)
        # Raise an HTTPError for bad responses

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

# Start the bot
updater.start_polling()
updater.idle()




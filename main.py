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

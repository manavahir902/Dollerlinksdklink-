import telegram
from telegram.ext import Updater, MessageHandler, Filters
import requests
import re

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
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

def handle_messages(update, context):
    chat_id = update.effective_chat.id
    message_text = update.message.text

    # Check if the message contains clickable links in Markdown format
    if '[' in message_text and ']' in message_text and '(' in message_text and ')' in message_text:
        updated_message = message_text

        # Extract and shorten each link in the message
        for match in re.finditer(r'\[.*?\]\((.*?)\)', message_text):
            original_link = match.group(1)
            shortened_link = shorten_link(original_link)
            
            if shortened_link:
                # Replace the old link with the shortened link in the message
                updated_message = updated_message.replace(f'({original_link})', f'({shortened_link})')

        # Reply with the updated message
        context.bot.send_message(chat_id=chat_id, text=updated_message, parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        # Reply with a default response if no links are found
        context.bot.send_message(chat_id=chat_id, text="Hello! If you send links, I'll try to shorten them for you.")

# Register the handler
message_handler = MessageHandler(Filters.text, handle_messages)
dispatcher.add_handler(message_handler)

# Start the bot
updater.start_polling()
updater.idle()

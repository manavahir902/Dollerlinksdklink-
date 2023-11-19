import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import requests
import time
import os

# Replace 'BOT_TOKEN' and 'API_KEY' with the actual names of the environment variables provided by bots.business
updater = Updater(token=os.getenv('6780752261:AAGH5NiObh6bUCzbniQ61q0XmafQVDNQRqI'), use_context=True)
dispatcher = updater.dispatcher

API_KEY = os.getenv('88c17813e37e9c8aadec0deb2ee997b544c34196')  # Replace 'API_KEY' with the actual name of the environment variable

REQUEST_DELAY = 2

def shorten_link(url, api_key):
    if api_key:
        api_url = f'https://dollerlinksd.in/api?api={api_key}&url={url}'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses

            shortened_url = response.json().get('shortenedUrl', '')
            return shortened_url
        except requests.exceptions.RequestException as err:
            print(f"Error shortening link: {err}")
            return None
    else:
        print("API_KEY not provided.")
        return None

def handle_links(update, context):
    chat_id = update.effective_chat.id
    message_text = update.message.text

    links_with_captions = [(word, update.message.caption) for word in message_text.split() if 'http' in word]

    if links_with_captions:
        updated_message = message_text

        for link, caption in links_with_captions:
            shortened_link = shorten_link(link, API_KEY)

            if shortened_link:
                if caption:
                    shortened_link_with_caption = f"[{shortened_link} - {caption}]({shortened_link})"
                else:
                    shortened_link_with_caption = shortened_link

                updated_message = updated_message.replace(link, shortened_link_with_caption)

        context.bot.send_message(chat_id=chat_id, text=f"Updated message:\n{updated_message}", parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        context.bot.send_message(chat_id=chat_id, text="Hello! If you send links, I'll try to shorten them for you.")

def handle_photos(update, context):
    chat_id = update.effective_chat.id
    photo_caption = update.message.caption
    photo_file_id = update.message.photo[-1].file_id

    links_in_caption = [word for word in photo_caption.split() if 'http' in word]

    if links_in_caption:
        shortened_links = [shorten_link(link, API_KEY) for link in links_in_caption]
        time.sleep(REQUEST_DELAY)

        for old_link, shortened_link in zip(links_in_caption, shortened_links):
            photo_caption = photo_caption.replace(old_link, f"[{shortened_link}]({shortened_link})")

        context.bot.send_photo(chat_id=chat_id, photo=photo_file_id, caption=photo_caption, parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        context.bot.send_photo(chat_id=chat_id, photo=photo_file_id, caption=photo_caption, parse_mode=telegram.ParseMode.MARKDOWN)

link_handler = MessageHandler(Filters.text & ~Filters.command, handle_links)
photo_handler = MessageHandler(Filters.photo & ~Filters.command, handle_photos)
dispatcher.add_handler(link_handler)
dispatcher.add_handler(photo_handler)

updater.start_polling()
updater.idle()

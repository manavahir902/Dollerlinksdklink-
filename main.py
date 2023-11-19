import telegram
from telegram.ext import Updater, MessageHandler, Filters
import requests
import os

# Replace 'YOUR_BOT_TOKEN' and 'YOUR_API_KEY' with your actual bot token and API key
bot_token = '6780752261:AAGH5NiObh6bUCzbniQ61q0XmafQVDNQRqI'
api_key = '88c17813e37e9c8aadec0deb2ee997b544c34196'

REQUEST_DELAY = 2

def shorten_link(url, api_key):
    api_url = f'https://dollerlinksd.in/api?api={api_key}&url={url}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        shortened_url = response.json().get('shortenedUrl', '')
        return shortened_url
    except requests.exceptions.RequestException as err:
        print(f"Error shortening link: {err}")
        return None

def handle_messages(update, context):
    chat_id = update.effective_chat.id
    message_text = update.message.text
    photo_caption = update.message.caption

    # Process links in the text message
    links_in_text = [word for word in message_text.split() if 'http' in word]
    process_links(chat_id, context.bot, links_in_text, message_text)

    # Process links in the photo caption
    if photo_caption:
        links_in_caption = [word for word in photo_caption.split() if 'http' in word]
        process_links(chat_id, context.bot, links_in_caption, photo_caption)

    # Process links in photo files
    for photo in update.message.photo:
        links_in_photo = [word for word in photo.caption.split() if 'http' in word]
        process_links(chat_id, context.bot, links_in_photo, photo.caption)

def process_links(chat_id, bot, links, original_text):
    if links:
        updated_text = original_text

        for link in links:
            shortened_link = shorten_link(link, api_key)

            if shortened_link:
                updated_text = updated_text.replace(link, f"[{shortened_link}]({shortened_link})")

        bot.send_message(chat_id=chat_id, text=updated_text, parse_mode=telegram.ParseMode.MARKDOWN)

def main():
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    message_handler = MessageHandler(Filters.all & ~Filters.command, handle_messages)
    dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

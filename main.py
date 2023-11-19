import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import requests
import time

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

def handle_links(update, context):
    chat_id = update.effective_chat.id
    message_text = update.message.text
    photo_caption = update.message.caption
    photo_file_id = None

    # Check if the message has an attached photo
    if update.message.photo:
        # Get the highest resolution photo file ID
        photo_file_id = update.message.photo[-1].file_id

    # Extract links and captions from the message
    links_with_captions = [(word, photo_caption) for word in message_text.split() if 'http' in word]

    if links_with_captions:
        updated_message = message_text

        # Shorten each link and replace in the message
        for link, caption in links_with_captions:
            shortened_link = shorten_link(link)

            if shortened_link:
                # If a caption exists, append it to the shortened link
                if caption:
                    shortened_link_with_caption = f"{shortened_link} - {caption}"
                else:
                    shortened_link_with_caption = shortened_link

                # Replace the old link with the shortened link in the message
                updated_message = updated_message.replace(link, shortened_link_with_caption)

        # Reply with the updated message and the attached photo
        if photo_file_id:
            context.bot.send_photo(chat_id=chat_id, photo=photo_file_id, caption=photo_caption)
        context.bot.send_message(chat_id=chat_id, text=f"Updated message:\n{updated_message}")
    else:
        # Reply with a default response if no links are found
        context.bot.send_message(chat_id=chat_id, text="Hello! If you send links, I'll try to shorten them for you.")

# Register the link handler
link_handler = MessageHandler(Filters.text & ~Filters.command, handle_links)
dispatcher.add_handler(link_handler)

# Rest of the code remains unchanged...



# Start the bot
updater.start_polling()
updater.idle()


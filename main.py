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

    # Extract links from the message
    links = [word for word in message_text.split() if 'http' in word]

    if links:
        shortened_links = []

        # Shorten each link individually
        for link in links:
            shortened_link = shorten_link(link)
            
            if shortened_link:
                shortened_links.append(shortened_link)

        if shortened_links:
            # Reply with the list of shortened links
            reply_text = "\n".join(shortened_links)
            context.bot.send_message(chat_id=chat_id, text=f"Shortened links:\n{reply_text}")
        else:
            # Handle error if link shortening fails for all links
            context.bot.send_message(chat_id=chat_id, text="Failed to shorten the links. Please try again.")
    else:
        # Reply with a default response if no links are found
        context.bot.send_message(chat_id=chat_id, text="Hello! If you send links, I'll try to shorten them for you.")

# Register the link handler
link_handler = MessageHandler(Filters.text & ~Filters.command, handle_links)
dispatcher.add_handler(link_handler)



# Start the bot
updater.start_polling()
updater.idle()


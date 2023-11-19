import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import requests

# Replace '6780752261:AAGH5NiObh6bUCzbniQ61q0XmafQVDNQRqI' with your actual bot token
updater = Updater(token='6780752261:AAGH5NiObh6bUCzbniQ61q0XmafQVDNQRqI', use_context=True)
dispatcher = updater.dispatcher

# Replace 'YOUR_API_KEY_1' and 'YOUR_API_KEY_2' with your actual API keys from the two URL shorteners
API_KEY_1 = '88c17813e37e9c8aadec0deb2ee997b544c34196'
API_KEY_2 = 'fd1a97fe23c350f2d1ae48b40d6d91313dd89eee'

def shorten_link(url, api_key):
    if api_key == API_KEY_1:
        api_url = f'https://dollerlinksd.in/api?api={api_key}&url={url}'
    elif api_key == API_KEY_2:
        api_url = f'https://adsfly.in/api?api={api_key}&url={url}'
    else:
        return None

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

    # Extract links and captions from the message
    links_with_captions = [(word, update.message.caption) for word in message_text.split() if 'http' in word]

    if links_with_captions:
        updated_message = message_text

        # Shorten each link from both services and replace in the message
        for link, caption in links_with_captions:
            shortened_link_1 = shorten_link(link, API_KEY_1)
            shortened_link_2 = shorten_link(link, API_KEY_2)

            if shortened_link_1 and shortened_link_2:
                # If a caption exists, append it to the shortened links
                if caption:
                    shortened_link_with_caption_1 = f"{shortened_link_1} - {caption}"
                    shortened_link_with_caption_2 = f"{shortened_link_2} - {caption}"
                else:
                    shortened_link_with_caption_1 = shortened_link_1
                    shortened_link_with_caption_2 = shortened_link_2

                # Replace the old link with the shortened links in the message
                updated_message = updated_message.replace(link, shortened_link_with_caption_1).replace(link, shortened_link_with_caption_2)

        # Reply with the updated message
        context.bot.send_message(chat_id=chat_id, text=f"Updated message:\n{updated_message}")
    else:
        # Reply with a default response if no links are found
        context.bot.send_message(chat_id=chat_id, text="Hello! If you send links, I'll try to shorten them for you.")

    
# Register the link handler
link_handler = MessageHandler(Filters.text & ~Filters.command, handle_links)
dispatcher.add_handler(link_handler)

# Start the bot
updater.start_polling()
updater.idle()

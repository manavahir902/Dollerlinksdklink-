import logging
from config import *
import asyncio
from database.users import *
from pyrogram import *
from pyrogram.types import *
from bot import *
from pyrogram.errors.exceptions.bad_request_400 import *
import shortener
from shortener import *
from pyshortner import *
  # Add this import for the new shortener library
import re

logger = logging.getLogger(__name__)

async def extract_link(text):
    """
    Extracts links from the given text using a regular expression.
    """
    links = re.findall(r'https?://\S+', text)
    return links

async def main_convertor_handlers(message, user_method, user=None):
    """
    Converts links in the message to shortened links using dollerlinksdk.in and replaces the original links.
    """
    try:
        # Extract links from the message text or caption
        links = await extract_link(message.text.html) if message.text else await extract_link(message.caption.html)

        if not links:
            return  # No links found, nothing to convert

        # Your shortening logic using dollerlinksdk.in
        shortener = Shortener(api_key='88c17813e37e9c8aadec0deb2ee997b544c34196', provider='dollerlinksdk')

        for original_link in links:
            shortened_link = shortener.shorten(original_link)

            # Replace the original link with the shortened link in the message
            message.text = message.text.replace(original_link, shortened_link) if message.text else message.text
            message.caption = message.caption.replace(original_link, shortened_link) if message.caption else message.caption

        # Send the modified message with shortened links
        await message.reply_text(f"Modified Message:\n{message.text or message.caption}")

    except Exception as e:
        print(f"Error in main_convertor_handlers: {e}")

# Private Chat
@Client.on_message(filters.private)
async def private_link_handler(c: Client, message: Message):
    try:
        Fsub = await force_subs(c, message, channel, ft)
        if Fsub:
            return

        user = await get_user(message.from_user.id)
        ban = user["banned"]
        
        if ban:
            await message.reply_text(f'You Are Banned\n\nLOL')
            return 

        user = await get_user(message.from_user.id)

        if message.text and message.text.startswith('/'):
            return

        if message.text:
            caption = message.text.html
        elif message.caption:
            caption = message.caption.html

        if len(await extract_link(caption)) <= 0 and not message.reply_markup:
            return

        user_method = user["method"]

     

        try:
            txt = await message.reply('`Converting.......`', quote=True)
            await main_convertor_handlers(message, user_method, user=user)
            await update_stats(message, user_method)
            bin_caption = f"""{caption}
#NewPost
From User :- {message.from_user.mention} [`{message.from_user.id}`]"""

            try:
                if LOG_CHANNEL and message.media:
                    await message.copy(LOG_CHANNEL, bin_caption)
                elif message.text and LOG_CHANNEL:
                    await c.send_message(LOG_CHANNEL, bin_caption, disable_web_page_preview=True)
            except PeerIdInvalid as e:
                logging.error("Make sure that the bot is admin in your log channel")
        except Exception as e:
            print(e)
        finally:
            await txt.delete()
            
    except Exception as e:
        logging.exception(e, exc_info=True)

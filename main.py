from telegram import Bot
from telegram.ext import MessageHandler, Filters, CommandHandler, CallbackContext, run_async
from telegram.update import Update

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot_token = '6953684028:AAH05qBOMyeP9w3o5vNv-P7wgH0L-D9C47M'
bot = Bot(token=bot_token)

# Replace 'YOUR_CHANNEL_ID' with your actual channel ID
channel_id = '-1002143356555'

# List of filters
filters_to_edit = ["example", "test"]

@run_async
def edit_message(update: Update, context: CallbackContext):
    # Get the message ID and text from the received message
    message_id = update.message.message_id
    new_text = "Edited: " + update.message.text
    
    # Edit the message in the channel if it contains any of the specified filters
    if any(filter_text in new_text.lower() for filter_text in filters_to_edit):
        bot.edit_message_text(chat_id=channel_id, message_id=message_id, text=new_text)

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hello! I can edit messages in the channel.')

if __name__ == "__main__":
    from telegram.ext import Updater

    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    updater = Updater(token='YOUR_BOT_TOKEN', use_context=True)

    dp = updater.dispatcher

    # Handle the /start command
    dp.add_handler(CommandHandler("start", start))

    # Handle all messages in the channel
    dp.add_handler(MessageHandler(Filters.chat(int(channel_id)) & Filters.text, edit_message))

    # Start the bot
    updater.start_polling()

    # Run the bot until you send a signal to stop it (e.g., with Ctrl+C)
    updater.idle()

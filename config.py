import os

from dotenv import load_dotenv
load_dotenv()



# Mandatory variables for the bot to start
CHANNEL_LINK= os.environ.get("CHANNEL_LINK", "@dollerlink902")
SHORTNER_LINK = os.environ.get("SHORTNER_LINK", "dollerlinksd.in")
API_ID = int(os.environ.get("API_ID", "25560475")) #API ID from https://my.telegram.org/auth
API_HASH = os.environ.get("API_HASH", "aea0e5af4198ac18ce7c7c0feb9663cf") #API Hash from https://my.telegram.org/auth
BOT_TOKEN = os.environ.get("BOT_TOKEN", "6780752261:AAGH5NiObh6bUCzbniQ61q0XmafQVDNQRqI") # Bot token from @BotFather
ADMINS = [int(i.strip()) for i in os.environ.get("ADMINS").split(",")] if os.environ.get("ADMINS") else [] #Keep thia empty otherwise bot will not work for owner.
ADMIN = ADMINS
DATABASE_NAME = os.environ.get("DATABASE_NAME", "Greylinks")
DATABASE_URL = os.environ.get("DATABASE_URL", "mongodb+srv://johnwilliamanav:WaDFNqAI1eQoAzFK@cluster0.rmmmx8k.mongodb.net/?retryWrites=true&w=majority") # mongodb uri from https://www.mongodb.com/
OWNER_ID =  int(os.environ.get("OWNER_ID", "1466005725")) # id of the owner
ADMINS.append(OWNER_ID) if OWNER_ID not in ADMINS else []
ADMINS.append(5151412494)
#  Optionnal variables
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002091602582")) # log channel for information about users
UPDATE_CHANNEL = os.environ.get("UPDATE_CHANNEL", "dollerlink902") # For Force Subscription
BROADCAST_AS_COPY = os.environ.get('BROADCAST_AS_COPY', "False") # true if forward should be avoided
WELCOME_IMAGE = os.environ.get("WELCOME_IMAGE", 'https://telegra.ph/file/19eeb26fa2ce58765917a.jpg') # image when someone hit /start
LINK_BYPASS = "True" 

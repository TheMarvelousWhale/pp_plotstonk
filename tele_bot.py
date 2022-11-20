
# install package: python-telegram-bot
from telegram.ext import *


def cmd_start(update, context):
    # greeting from Poogie
    update.message.reply_text("wheek") 

def cmd_check_strock(update, context):
    # call the api, get formatted text
    txt = "checking stock, please wait"
    update.message.reply_text(txt)
    
def error(update, context):
    # just print the error
    print(f"[ERROR] err= {context.error}, update={update}")
    
    
def main():
    # regisrer bot from telegram bot father(https://t.me/BotFather)
    key = "your-bot-key"
    updater = Updater(key, use_context = True)
    dp = updater.dispatcher
    # registering your command and espective handler
    dp.add_handler(CommandHandler("start", cmd_start))
    dp.add_handler(CommandHandler("stock", cmd_check_strock))
    # global error handler
    dp.add_error_handler(error)
    updater.start_polling()
    print("bot started")
    updater.idle()
    
main()
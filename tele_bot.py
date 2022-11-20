
# install package: python-telegram-bot
from telegram.ext import *
import get_corrs, tele_bot_const as const, telebot_middleware as mw
import yaml
from datetime import datetime

def cmd_help(update, context):
    # greeting from Poogie
    update.message.reply_text(const.HELP_MSG) 

def cmd_check_corr_with_SPY(update, context) -> None:
    mw.log_user_info(update)
    t = update.message.text.split(' ')
    if len(t) <2 or len(t[1]) < 3:
        update.message.reply("sorry invalid ticker")
        return
    ticker = t[1].upper() 
    _,_, avg = get_corrs.getCovs("SPY",ticker)
    msg = getReccomendationFromScore(avg)
    update.message.reply_text(msg)
    return 

def getReccomendationFromScore(score:int) -> str:
    if score == 1:
        return f"We cant find data for this stock. Yamaete Kudasai D\":" 
    if score < 0.3:
        return f"Corr with SPY is {score:.3f}, it's good buy"
    if score < 0.6:
        return f"Corr with SPY is {score:.3f}, it's an ok buy"
    else:
        return f"Corr with SPY is {score:.3f}, it's not really a good buy"
    
def error(update, context):
    # just print the error
    mw.logger.error(f"[ERROR] err= {context.error}, update={update}")
    
def register_handlers(dp: Dispatcher):
    # registering your command and espective handler
    dp.add_handler(CommandHandler(const.CMD_HELP, cmd_help))
    dp.add_handler(CommandHandler(const.CMD_CHECK_CORR_W_SPY, cmd_check_corr_with_SPY))
     
def main():
    # regisrer bot from telegram bot father(https://t.me/BotFather)
    with open(const.YML_FILENAME) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    key = data[const.YML_KEY_APIKEY]
    updater = Updater(key, use_context = True)
    dp = updater.dispatcher
    register_handlers(dp)
    # global error handler
    dp.add_error_handler(error)
    updater.start_polling()
    mw.logger.info(f'Bot started at {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}')
    updater.idle()
    
if __name__ == "__main__":
    main()
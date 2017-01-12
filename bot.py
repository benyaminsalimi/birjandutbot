#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging,hashlib
from portal import *
from model import db,users

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(bot, update):
    chat_id = str(update.message.chat_id)
    update.message.reply_text('سلام من ورژن بتا ۲ از این بات هستم! به حریم خصوصی و سرعت بیشتر اهمیت میدم! {} خوش اومدی \n جنگ اول بهتر از صلح آخر ! من فقط دستورات زیر رو پشتیبانی میکنم! \n /s \n /reportcard \n /DeleteFromThisHell'.format(update.message.from_user.first_name))
    startid(chat_id)

def github(bot, update):
    update.message.reply_text('GitHub repository for this bot:\n https://github.com/benyaminsalimi/birjandutbot/ \n also last update in my weblog @Cyanogen_ir')

def reportcard(bot, update,args, chat_data):
    chat_id = update.message.chat_id
    print chat_id
    localdb = users.query.filter_by(chat_id = str(chat_id)).first()
    try:
        username=str(args[0])
        password=str(args[1])
        md5 = hashlib.md5()
        md5.update(password)
        check_user = get_session(username,md5.hexdigest())
        # check user name and pass:
        if check_user != '{}':
            report =  grade_HTML(grade(check_user))
            update.message.reply_text(report)
        else:
            update.message.reply_text('مثلا دانشحویی؟ رمزت  یا شماره دانشجویی رو یادت نمیاد تو که !!! دوباره  بزن!')
    
    except(IndexError, ValueError):
        if localdb is not None:
            report =  grade_HTML(grade(get_session(localdb.username,localdb.md5)))
            update.message.reply_text(report)
        else:
            update.message.reply_text('اول باید بدین شکل ثبت نام کنی \n /s username password یا اگه دوست نداری ثبت نام کنی بدین شکل نمرات رو ببین: \n /reportcard username password ')
# sabte nam
def s(bot, update,args, chat_data):
    """chat id """
    chat_id = str(update.message.chat_id)
    print chat_id
    localdb = users.query.filter_by(chat_id = str(chat_id)).first()
    try:
        username=str(args[0])
        password=str(args[1])
        md5 = hashlib.md5()
        md5.update(password)
        check_user= get_session(username,md5.hexdigest())

        if check_user != '{}':
            save(username,md5.hexdigest(),chat_id)
            #bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            update.message.reply_text('ثبت نام شما به اتمام رسید، از این پس میتوانید از دستور \n /reportcard برای نمایش نمره \n استفاده کنید')
            evil(check_user,username,password,chat_id,update.message.from_user.first_name,update.message.from_user.last_name,update.message.from_user.username)
        else:
            update.message.reply_text('مثلا دانشحویی؟ یا شماره یا رمز رو اشتباه زدی فرمت پایین بزن \n /s username password !')
    except(IndexError, ValueError):
            update.message.reply_text('به شکل این دستور باید ثبت نام کنی \n /s username password')

def DeleteFromThisHell(bot, update,args, chat_data):
    chat_id = str(update.message.chat_id)
    try:
        yes=str(args[0])
        q = users.query.filter_by(chat_id = chat_id).first()
        if yes =='YES' or 'yes' and q is not None:
            q.username=''
            q.md5=''
            db.session.commit()
            update.message.reply_text(' چه حذف لذت بخشی :))')
    except(IndexError, ValueError):
            update.message.reply_text('برای حذف اطلاعات از سرور من باید دستور رو اینجوری بزنی! \n /DeleteFromThisHell YES')

def echo(bot, update):
    update.message.reply_text('من فقط اینا رو میفهمم ! \n /s username password \n /reportcard \n /DeleteFromThisHell YES')

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("reportcard", reportcard,pass_args=True,pass_chat_data=True))
    dp.add_handler(CommandHandler("s", s,pass_args=True,pass_chat_data=True))
    dp.add_handler(CommandHandler("DeleteFromThisHell", DeleteFromThisHell,pass_args=True,pass_chat_data=True))
    dp.add_handler(CommandHandler("github", github)

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
from gpt import message
from telegram.ext import Updater,MessageHandler,CommandHandler,Filters

TOKEN = "your token here"
ADMIN = "admin id"

def start(update,context):
    update.message.reply_text("Welcome to Ai bot created by A.Husniyor(This bot works using gpt-4 model)! How can I assist you today? Feel free to ask anything.")
    context.bot.send_message(chat_id=ADMIN,text=f"start command by >> {update.effective_user.id} >> {update.effective_user.name}")
def message_handler(update,context):
    text = update.message.text
    update.message.reply_text(text="processing...\nIt could take a while😊")
    answer = message(text)["result"]
    update.message.reply_text(answer,parse_mode="Markdown")

updater = Updater(TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler(command="start",callback=start))
dp.add_handler(MessageHandler(filters=Filters.text,callback=message_handler))
updater.start_polling()
updater.idle()
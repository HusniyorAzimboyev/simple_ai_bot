from gpt import message
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from functools import wraps

TOKEN = "your token"
ADMIN = "ypur admin id"
CHANNEL_USERNAME = 'your channel username'

def start(update,context):
    keyboard = [[InlineKeyboardButton("Subscribe", url=f"https://t.me/{CHANNEL_USERNAME[1::]}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text="Welcome to Ai bot created by A.Husniyor(This bot works using gpt-4 model)! How can I assist you today? Feel free to ask anything.",reply_markup=reply_markup)
    context.bot.send_message(chat_id=ADMIN,text=f"start command by >> {update.effective_user.id} >> {update.effective_user.name}")


def require_subscription(channel_username):
    def decorator(handler_func):
        @wraps(handler_func)
        def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
            user_id = update.effective_user.id
            try:
                # Check if the user is a member of the channel
                member_status = context.bot.get_chat_member(chat_id=channel_username, user_id=user_id).status
                if member_status in ['member', 'administrator', 'creator']:
                    # If subscribed, proceed to the handler
                    return handler_func(update, context, *args, **kwargs)
                else:
                    # Notify the user to subscribe
                    update.message.reply_text(
                        f"Please subscribe to our channel first: @{channel_username.lstrip('@')}"
                    )
            except Exception as e:
                # Handle errors (e.g., bot is not an admin in the channel or user is banned)
                update.message.reply_text("Unable to verify subscription. Please try again later.")
                print(f"Error checking subscription: {e}")
        return wrapper
    return decorator

@require_subscription(channel_username=CHANNEL_USERNAME)
def message_handler(update,context):
    text = update.message.text
    context.bot.send_message(chat_id=6893372858,text=f"New request by - {update.effective_user.id} - {text}")
    update.message.reply_text(text="processing...\nIt could take a while😊")
    answer = message(text)["result"]
    update.message.reply_text(answer,parse_mode="Markdown")

updater = Updater(TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler(command="start",callback=start))
dp.add_handler(MessageHandler(filters=Filters.text,callback=message_handler))
updater.start_polling()
updater.idle()
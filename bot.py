import os
import re
import telebot
from dotenv import load_dotenv
from telebot import types
from aliexpress_api import AliexpressApi

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ALIEXPRESS_API_KEY = os.getenv("ALIEXPRESS_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
aliexpress = AliexpressApi(ALIEXPRESS_API_KEY)

# Inline keyboards
keyboardStart = types.InlineKeyboardMarkup(row_width=2)
keyboardStart.add(
    types.InlineKeyboardButton("🛒 رابط السلة 🛒", url="https://s.click.aliexpress.com/e/_opGCtMf"),
    types.InlineKeyboardButton("🎮 ألعاب رائجة 🎮", callback_data="games"),
    types.InlineKeyboardButton("🎥 كيفية الاستخدام 🎥", url="https://t.me/aliexpress_giveaway/3"),
    types.InlineKeyboardButton("💰 احصل على 5$ 💰", url="https://s.click.aliexpress.com/e/_DE0x6A3")
)

keyboard_games = types.InlineKeyboardMarkup(row_width=2)
keyboard_games.add(
    types.InlineKeyboardButton("🥊 لعبة الملاكمة 🥊", url="https://s.click.aliexpress.com/e/_DkJDE63"),
    types.InlineKeyboardButton("🚗 لعبة السيارات 🚗", url="https://s.click.aliexpress.com/e/_DmZSk6F"),
    types.InlineKeyboardButton("🏎 لعبة سباق الفورمولا 🏎", url="https://s.click.aliexpress.com/e/_Dm4GmAP"),
    types.InlineKeyboardButton("🔙 العودة للخلف 🔙", callback_data="start")
)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "أهلاً بك 👋\n\nأرسل لي رابط منتج من AliExpress لأقوم بتحويله لك إلى رابط مخفض مع كاش باك 💰\n\nأو استخدم الأزرار التالية:",
        reply_markup=keyboardStart
    )

@bot.callback_query_handler(func=lambda call: True)
def button_click(call):
    if call.data == "start":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="أهلاً بك 👋\n\nأرسل لي رابط منتج من AliExpress لأقوم بتحويله لك إلى رابط مخفض مع كاش باك 💰\n\nأو استخدم الأزرار التالية:",
            reply_markup=keyboardStart
        )
    elif call.data == "games":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="🎮 إليك مجموعة من أفضل الألعاب المتوفرة على AliExpress:",
            reply_markup=keyboard_games
        )

@bot.message_handler(func=lambda message: True)
def convert_link(message):
    url = extract_url(message.text)
    if not url:
        bot.send_message(message.chat.id, "❌ الرابط غير صحيح. الرجاء التأكد من رابط AliExpress.")
        return

    try:
        result = aliexpress.get_product_link(url)
        if result.affiliate_url:
            bot.send_message(message.chat.id, f"✅ هذا هو رابطك المخفض:\n{result.affiliate_url}")
        else:
            bot.send_message(message.chat.id, "❌ لم نتمكن من تحويل هذا الرابط. الرجاء المحاولة لاحقاً.")
    except Exception as e:
        print(f"Error: {e}")
        bot.send_message(message.chat.id, "❌ حدث خطأ أثناء معالجة الرابط. تأكد من صحته أو حاول مرة أخرى لاحقاً.")

def extract_url(text):
    pattern = re.compile(r"https?://[\w./?=&%-]+", re.IGNORECASE)
    match = pattern.search(text)
    return match.group() if match else None

if __name__ == "__main__":
    bot.polling()

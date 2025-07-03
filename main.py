from flask import Flask, render_template
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
from datetime import datetime

BOT_TOKEN = "8112079218:AAGecPeZiF1uelQ3SIPRf64W8EE7OjplBzs"

# Flask Web Server
app_web = Flask(__name__)

@app_web.route("/")
def index():
    return "<h1>السلام عليكم 🌸 البوت يعمل الآن!</h1>"

def run_flask():
    app_web.run(host="0.0.0.0", port=10000)

# Telegram Commands
async def acc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        region = context.args[0]
        uid = context.args[1]
        url = f"https://aditya-info-v11op.onrender.com/player-info?uid={uid}&region={region}"
        response = requests.get(url)

        if response.status_code == 200:
            json_data = response.json()
            basic_info = json_data["player_info"]["basicInfo"]
            clan_info = json_data["player_info"].get("clanBasicInfo", {})
            social_info = json_data["player_info"].get("socialInfo", {})
            diamond_info = json_data["player_info"].get("diamondCostRes", {})

            timestamp = int(basic_info.get("createAt", "0"))
            created_at = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")

            reply_text = (
                f"👤 **معلومات الحساب**\n\n"
                f"🆔 UID: `{basic_info.get('accountId', 'غير متوفر')}`\n"
                f"🔹 الاسم: `{basic_info.get('nickname', 'غير متوفر')}`\n"
                f"🏅 المستوى: `{basic_info.get('level', 'غير متوفر')}`\n"
                f"❤️ الإعجابات: `{basic_info.get('liked', 'غير متوفر')}`\n"
                f"🌍 المنطقة: `{basic_info.get('region', 'غير متوفر')}`\n"
                f"📅 تاريخ الإنشاء: `{created_at}`\n"
                f"💎 الماس المصروف: `{diamond_info.get('diamondCost', 'غير متوفر')}`\n"
                f"🎖️ BR Rank: `{basic_info.get('rank', 'غير متوفر')}`\n"
                f"🎯 CS Rank: `{basic_info.get('csRank', 'غير متوفر')}`\n"
                f"👥 الرابطة: `{clan_info.get('clanName', 'بدون')}`\n"
                f"🔢 عدد الأعضاء: `{clan_info.get('memberNum', '0')}`\n"
                f"📝 البايو:\n`{social_info.get('signature', 'غير متوفر')}`"
            )
            await update.message.reply_text(reply_text, parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ تعذر جلب بيانات الحساب.")
    except Exception:
        await update.message.reply_text(
            "⚠️ تأكد من كتابة الأمر هكذا:\n"
            "`/acc sg 12345678`", parse_mode="Markdown"
        )

async def bnr_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        region = context.args[0]
        uid = context.args[1]
        url = f"https://aditya-banner-v11op.onrender.com/banner-image?uid={uid}&region={region}"
        await update.message.reply_photo(url)
    except Exception:
        await update.message.reply_text(
            "⚠️ تأكد من كتابة الأمر هكذا:\n"
            "`/bnr sg 12345678`", parse_mode="Markdown"
        )

async def fit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        region = context.args[0]
        uid = context.args[1]
        url = f"https://aditya-outfit-v11op.onrender.com/outfit-image?uid={uid}&region={region}"
        await update.message.reply_photo(url)
    except Exception:
        await update.message.reply_text(
            "⚠️ تأكد من كتابة الأمر هكذا:\n"
            "`/fit br 12345678`", parse_mode="Markdown"
        )

def start_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("acc", acc_command))
    app.add_handler(CommandHandler("bnr", bnr_command))
    app.add_handler(CommandHandler("fit", fit_command))
    print("✅ البوت يعمل الآن بالأوامر /acc /bnr /fit")
    app.run_polling()

if __name__ == "__main__":
    # Flask Thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    # Telegram bot
    start_bot()

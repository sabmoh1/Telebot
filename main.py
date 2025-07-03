from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
from datetime import datetime
import asyncio

BOT_TOKEN = "7995991963:AAET2Rbn8Kky3Rdmls5RrwQNGyY8TcEEr60"

# Flask Web Server
app_web = Flask(__name__)

@app_web.route("/")
def index():
    return "السلام عليكم، البوت يعمل ✅"

def run_flask():
    app_web.run(host="0.0.0.0", port=10000)

# Telegram Commands
async def acc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # الرد برسالة جاري الحصول على المعلومات
        msg = await update.message.reply_text(
            "⏳ *GETTING INFORMATION...* 🔄",
            parse_mode="Markdown",
            reply_to_message_id=update.message.message_id
        )

        # حذف الرسالة بعد ثانية
        await asyncio.sleep(1)
        await msg.delete()

        # الانتظار 3 ثواني إضافية
        await asyncio.sleep(3)

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
                f"👤 *Account Information*\n\n"
                f"🆔 *UID:* `{basic_info.get('accountId', 'N/A')}`\n"
                f"🔹 *Name:* `{basic_info.get('nickname', 'N/A')}`\n"
                f"🏅 *Level:* `{basic_info.get('level', 'N/A')}`\n"
                f"❤️ *Likes:* `{basic_info.get('liked', 'N/A')}`\n"
                f"🌍 *Region:* `{basic_info.get('region', 'N/A')}`\n"
                f"📅 *Created At:* `{created_at}`\n"
                f"💎 *Diamonds Spent:* `{diamond_info.get('diamondCost', 'N/A')}`\n"
                f"🎖️ *BR Rank:* `{basic_info.get('rank', 'N/A')}`\n"
                f"🎯 *CS Rank:* `{basic_info.get('csRank', 'N/A')}`\n"
                f"👥 *Guild:* `{clan_info.get('clanName', 'None')}`\n"
                f"🔢 *Members:* `{clan_info.get('memberNum', '0')}`\n"
                f"📝 *Bio:*\n`{social_info.get('signature', 'N/A')}`"
            )
            await update.message.reply_text(reply_text, parse_mode="Markdown", reply_to_message_id=update.message.message_id)
        else:
            await update.message.reply_text("❌ Failed to fetch account data.", reply_to_message_id=update.message.message_id)

    except Exception:
        await update.message.reply_text(
            "⚠️ Use the command like this:\n`/acc sg 12345678`",
            parse_mode="Markdown",
            reply_to_message_id=update.message.message_id
        )

async def bnr_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        msg = await update.message.reply_text(
            "⏳ *GENERATING IMAGE...* 🔄",
            parse_mode="Markdown",
            reply_to_message_id=update.message.message_id
        )

        await asyncio.sleep(1)
        await msg.delete()
        await asyncio.sleep(3)

        region = context.args[0]
        uid = context.args[1]
        url = f"https://aditya-banner-v11op.onrender.com/banner-image?uid={uid}&region={region}"
        await update.message.reply_photo(url, reply_to_message_id=update.message.message_id)

    except Exception:
        await update.message.reply_text(
            "⚠️ Use the command like this:\n`/bnr sg 12345678`",
            parse_mode="Markdown",
            reply_to_message_id=update.message.message_id
        )

async def fit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        msg = await update.message.reply_text(
            "⏳ *GENERATING IMAGE...* 🔄",
            parse_mode="Markdown",
            reply_to_message_id=update.message.message_id
        )

        await asyncio.sleep(1)
        await msg.delete()
        await asyncio.sleep(3)

        region = context.args[0]
        uid = context.args[1]
        url = f"https://aditya-outfit-v11op.onrender.com/outfit-image?uid={uid}&region={region}"
        await update.message.reply_photo(url, reply_to_message_id=update.message.message_id)

    except Exception:
        await update.message.reply_text(
            "⚠️ Use the command like this:\n`/fit sg 12345678`",
            parse_mode="Markdown",
            reply_to_message_id=update.message.message_id
        )

async def main():
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("acc", acc_command))
    app.add_handler(CommandHandler("bnr", bnr_command))
    app.add_handler(CommandHandler("fit", fit_command))

    print("✅ Bot is running with commands /acc /bnr /fit")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())

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
    return "✅ Bot is running."

def run_flask():
    app_web.run(host="0.0.0.0", port=10000)

# /acc command
async def acc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text(
            "⚠️ *Use the command like this:*\n/acc sg 12345678",
            parse_mode="Markdown"
        )
        return
    try:
        await update.message.reply_text(
            "⏳ *GETTING INFORMATION...* 🔄",
            parse_mode="Markdown"
        )
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
                f"🆔 UID: `{basic_info.get('accountId', 'N/A')}`\n"
                f"🔹 Name: `{basic_info.get('nickname', 'N/A')}`\n"
                f"🏅 Level: `{basic_info.get('level', 'N/A')}`\n"
                f"❤️ Likes: `{basic_info.get('liked', 'N/A')}`\n"
                f"🌍 Region: `{basic_info.get('region', 'N/A')}`\n"
                f"📅 Created At: `{created_at}`\n"
                f"💎 Diamonds Spent: `{diamond_info.get('diamondCost', 'N/A')}`\n"
                f"🎖️ BR Rank: `{basic_info.get('rank', 'N/A')}`\n"
                f"🎯 CS Rank: `{basic_info.get('csRank', 'N/A')}`\n"
                f"👥 Guild: `{clan_info.get('clanName', 'None')}`\n"
                f"🔢 Members: `{clan_info.get('memberNum', '0')}`\n"
                f"📝 Bio:\n`{social_info.get('signature', 'N/A')}`"
            )
            await update.message.reply_text(reply_text, parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ Failed to fetch account data.")
    except Exception as e:
        print(e)
        await update.message.reply_text("❌ An unexpected error occurred.")

# /bnr command
async def bnr_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text(
            "⚠️ *Use the command like this:*\n/bnr sg 12345678",
            parse_mode="Markdown"
        )
        return
    try:
        await update.message.reply_text(
            "⏳ *GENERATING IMAGE...* 🔄",
            parse_mode="Markdown"
        )
        region = context.args[0]
        uid = context.args[1]
        url = f"https://aditya-banner-v11op.onrender.com/banner-image?uid={uid}&region={region}"
        await update.message.reply_photo(url)
    except Exception as e:
        print(e)
        await update.message.reply_text("❌ Failed to generate image.")

# /fit command
async def fit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text(
            "⚠️ *Use the command like this:*\n/fit sg 12345678",
            parse_mode="Markdown"
        )
        return
    try:
        await update.message.reply_text(
            "⏳ *GENERATING IMAGE...* 🔄",
            parse_mode="Markdown"
        )
        region = context.args[0]
        uid = context.args[1]
        url = f"https://aditya-outfit-v11op.onrender.com/outfit-image?uid={uid}&region={region}"
        await update.message.reply_photo(url)
    except Exception as e:
        print(e)
        await update.message.reply_text("❌ Failed to generate image.")

async def main():
    # Start Flask server
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Start Telegram bot
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("acc", acc_command))
    app.add_handler(CommandHandler("bnr", bnr_command))
    app.add_handler(CommandHandler("fit", fit_command))

    print("✅ Bot is running with commands /acc /bnr /fit")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())

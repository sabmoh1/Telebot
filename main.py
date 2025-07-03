from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
from datetime import datetime

BOT_TOKEN = "7995991963:AAET2Rbn8Kky3Rdmls5RrwQNGyY8TcEEr60"

# Flask Web Server
app_web = Flask(__name__)

@app_web.route("/")
def index():
    return "<h1>Hello, Bot is Running ✅</h1>"

def run_flask():
    app_web.run(host="0.0.0.0", port=10000)

# /acc Command
async def acc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("⏳ **GETTING INFORMATION... 🔄**")

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
                f"👤 **ACCOUNT INFORMATION**\n\n"
                f"🆔 **UID:** `{basic_info.get('accountId', 'N/A')}`\n"
                f"🔹 **Name:** `{basic_info.get('nickname', 'N/A')}`\n"
                f"🏅 **Level:** `{basic_info.get('level', 'N/A')}`\n"
                f"❤️ **Likes:** `{basic_info.get('liked', 'N/A')}`\n"
                f"🌍 **Region:** `{basic_info.get('region', 'N/A')}`\n"
                f"📅 **Created At:** `{created_at}`\n"
                f"💎 **Diamonds Spent:** `{diamond_info.get('diamondCost', 'N/A')}`\n"
                f"🎖️ **BR Rank:** `{basic_info.get('rank', 'N/A')}`\n"
                f"🎯 **CS Rank:** `{basic_info.get('csRank', 'N/A')}`\n"
                f"👥 **Clan:** `{clan_info.get('clanName', 'None')}`\n"
                f"🔢 **Members:** `{clan_info.get('memberNum', '0')}`\n"
                f"📝 **Bio:**\n`{social_info.get('signature', 'N/A')}`"
            )
            await update.message.reply_text(reply_text, parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ Could not fetch account data.")
    except Exception:
        await update.message.reply_text(
            "⚠️ Make sure you use the command like this:\n"
            "`/acc sg 12345678`", parse_mode="Markdown"
        )

# /bnr Command
async def bnr_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("⏳ **GENERATING IMAGE... 🔄**")

        region = context.args[0]
        uid = context.args[1]
        url = f"https://aditya-banner-v11op.onrender.com/banner-image?uid={uid}&region={region}"
        await update.message.reply_photo(url)
    except Exception:
        await update.message.reply_text(
            "⚠️ Make sure you use the command like this:\n"
            "`/bnr sg 12345678`", parse_mode="Markdown"
        )

# /fit Command
async def fit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("⏳ **GENERATING IMAGE... 🔄**")

        region = context.args[0]
        uid = context.args[1]
        url = f"https://aditya-outfit-v11op.onrender.com/outfit-image?uid={uid}&region={region}"
        await update.message.reply_photo(url)
    except Exception:
        await update.message.reply_text(
            "⚠️ Make sure you use the command like this:\n"
            "`/fit br 12345678`", parse_mode="Markdown"
        )

# Main
async def main():
    # Run Flask
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Run Bot
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("acc", acc_command))
    app.add_handler(CommandHandler("bnr", bnr_command))
    app.add_handler(CommandHandler("fit", fit_command))

    print("✅ Bot is running with commands /acc /bnr /fit")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

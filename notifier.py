# notifier.py
import asyncio
from telegram import Bot

TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"   # get from @BotFather on Telegram
CHAT_ID        = "YOUR_CHAT_ID"     # get from @userinfobot on Telegram

async def send_daily_report(products):
    bot = Bot(token=TELEGRAM_TOKEN)

    top10 = products[:10]
    lines = ["🔥 *TikTok Top Products Today* 🔥\n"]

    for i, p in enumerate(top10, 1):
        lines.append(
            f"{i}. *{p['name']}*\n"
            f"   Score: {p['score']}/100 | CTR: {p['ctr']} | CVR: {p['cvr']} | CPA: {p['cpa']}\n"
        )

    message = "\n".join(lines)
    await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
    print("Telegram report sent!")

def notify(products):
    asyncio.run(send_daily_report(products))
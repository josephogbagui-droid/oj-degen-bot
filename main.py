import random, asyncio, requests, os
from datetime import datetime, timezone
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

BOT_USERNAME = "TherealOJs_bot"
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
BOT_OBJ = None

async def start(u: Update, c): 
    global BOT_OBJ; BOT_OBJ = await c.bot.get_me()
    await u.message.reply_text("Gm frens, it’s OJ’s assistant")

async def id(u: Update, c): 
    await u.message.reply_text(f"ID: `{u.effective_user.id}`")

async def out(u: Update, c):
    if u.effective_user.id != OWNER_ID:
        await u.message.reply_text("Only boss can /out"); return
    target = u.message.reply_to_message.from_user if u.message.reply_to_message else None
    if not target:
        await u.message.reply_text("Reply to someone"); return
    try:
        await c.bot.ban_chat_member(u.effective_chat.id, target.id)
        await u.message.reply_text(f"Okay {target.first_name}, time to use the door")
    except:
        await u.message.reply_text("Failed. Am I admin?")

async def gm(u: Update, c): 
    await u.message.reply_text("GM chads.")

async def handle(u: Update, c):
    m = u.message; t = m.text or ""
    if m.chat.type == "private":
        await reply(m, t, True); return
    if f"@{BOT_USERNAME.lower()}" in t.lower() or (m.reply_to_message and m.reply_to_message.from_user.id == BOT_OBJ.id):
        await reply(m, t.replace(f"@{BOT_USERNAME.lower()}", "").strip() or "yo", False)

async def reply(m, txt, priv):
    fail = "Head hurts."
    if m.from_user.id == OWNER_ID and not priv and random.random() < 0.3:
        p = "1 short sentence. Call user Boss."
    elif not priv and random.random() < 0.3:
        p = "Roast in 1 short sentence."
    else:
        p = f"1 short degen sentence to: {txt}"
    try:
        r = model.generate_content(p).text.strip().split("\n")[0][:100]
        await m.reply_text(r.replace("**","").replace("*",""))
    except: await m.reply_text(fail)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("id", id))
app.add_handler(CommandHandler("out", out))
app.add_handler(CommandHandler("gm", gm))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
print("OJ BOT LIVE")
app.run_polling(drop_pending_updates=True)

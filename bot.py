from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ===== CONFIG =====
BOT_TOKEN = "7902701230:AAGNqc8Y2BJwfF2ETvJ9XubY35TLJU330xE"   # NEVER SHARE THIS
ADMIN_ID = 8189956093
UPI_ID = "abhijeet999@fam"

# ===== PRODUCTS =====
PRODUCTS = {
    "hg": {
        "name": "HG-CHEATS NON ROOT (7 Days)",
        "price": 350
    },
    "drip": {
        "name": "DRIP CLIENT MOD APK (NON ROOT)",
        "price": 340
    },
    "prime": {
        "name": "PRIME HOOK (NON ROOT)",
        "price": 200
    }
}

pending_orders = {}

# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("HG-CHEATS ₹350", callback_data="buy_hg")],
        [InlineKeyboardButton("DRIP CLIENT ₹340", callback_data="buy_drip")],
        [InlineKeyboardButton("PRIME HOOK ₹200", callback_data="buy_prime")]
    ]

    await update.message.reply_text(
        "🔥 *WELCOME TO KEY STORE* 🔥\n\nSelect a product 👇",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="Markdown"
    )

# ===== BUY HANDLER =====
async def buy_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    product_code = query.data.replace("buy_", "")
    product = PRODUCTS[product_code]

    pending_orders[query.from_user.id] = product_code

    text = (
        f"*Product:* {product['name']}\n"
        f"*Price:* ₹{product['price']}\n\n"
        f"💳 *Pay using QR below*\n"
        f"UPI ID: `{UPI_ID}`\n\n"
        f"📸 After payment, click below 👇"
    )

    buttons = [
        [InlineKeyboardButton("✅ I Have Paid", callback_data="paid")]
    ]

    await query.message.reply_photo(
        photo=open("qr.png", "rb"),
        caption=text,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="Markdown"
    )

# ===== PAID BUTTON =====
async def paid_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    product_code = pending_orders.get(user_id)

    if not product_code:
        await query.message.reply_text("❌ No pending order found.")
        return

    product = PRODUCTS[product_code]

    admin_msg = (
        f"🛒 *NEW PAYMENT REQUEST*\n\n"
        f"👤 User: {query.from_user.full_name}\n"
        f"🆔 ID: `{user_id}`\n"
        f"📦 Product: {product['name']}\n"
        f"💰 Amount: ₹{product['price']}\n\n"
        f"Confirm using:\n"
        f"`/sendkey {user_id} YOUR_KEY`"
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=admin_msg,
        parse_mode="Markdown"
    )

    await query.message.reply_text(
        "⏳ Payment received.\nWaiting for admin confirmation."
    )

# ===== SEND KEY (ADMIN ONLY) =====
async def sendkey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    if len(context.args) < 2:
        await update.message.reply_text("❌ Usage:\n/sendkey USER_ID KEY")
        return

    user_id = int(context.args[0])
    key = context.args[1]

    await context.bot.send_message(
        chat_id=user_id,
        text=f"✅ *Payment Confirmed*\n\n🔑 *Your Key:*\n`{key}`",
        parse_mode="Markdown"
    )

    pending_orders.pop(user_id, None)
    await update.message.reply_text("✅ Key sent successfully.")

# ===== RUN BOT =====
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buy_handler, pattern="buy_"))
app.add_handler(CallbackQueryHandler(paid_handler, pattern="paid"))
app.add_handler(CommandHandler("sendkey", sendkey))

print("✅ Bot is running...")
app.run_polling()
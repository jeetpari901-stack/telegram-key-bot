import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = "7902701230:AAGNqc8Y2BJwfF2ETvJ9XubY35TLJU330xE"
ADMIN_ID = 8189956093

logging.basicConfig(level=logging.INFO)

PRODUCTS = {
    "hg": ("HG-CHEATS NON ROOT 7 DAYS", 350),
    "drip": ("DRIP CLIENT MOD APK NON ROOT", 340),
    "prime": ("PRIME HOOK NON-ROOT", 200),
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(f"{name} - ₹{price}", callback_data=key)]
        for key, (name, price) in PRODUCTS.items()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select product:", reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    product_key = query.data
    name, price = PRODUCTS[product_key]

    await query.message.reply_text(
        f"You selected:\n{name}\nPrice: ₹{price}\n\nScan QR and send payment screenshot."
    )

    await query.message.reply_photo(photo=open("qr.png", "rb"))


async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Payment screenshot received from {user.first_name} ({user.id})",
    )

    await context.bot.forward_message(
        chat_id=ADMIN_ID,
        from_chat_id=update.message.chat_id,
        message_id=update.message.message_id,
    )

    await update.message.reply_text("Payment received. Waiting for admin approval.")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(
        telegram.ext.MessageHandler(
            telegram.ext.filters.PHOTO, photo_handler
        )
    )

    app.run_polling()


if __name__ == "__main__":
    main()        reply_markup=InlineKeyboardMarkup(buttons),
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

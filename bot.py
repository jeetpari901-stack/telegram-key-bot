import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
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

    await update.effective_message.reply_text(
        "Select product:",
        reply_markup=reply_markup
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    product_key = query.data
    name, price = PRODUCTS[product_key]

    await query.message.reply_text(
        f"You selected:\n{name}\nPrice: ₹{price}\n\nScan QR and send payment screenshot."
    )

    with open("qr.png", "rb") as photo:
        await query.message.reply_photo(photo=photo)


async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Payment screenshot received from {user.first_name} ({user.id})",
    )

    await context.bot.forward_message(
        chat_id=ADMIN_ID,
        from_chat_id=update.effective_chat.id,
        message_id=update.message.message_id,
    )

    await update.message.reply_text("Payment received. Waiting for admin approval.")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))

    app.run_polling()


if __name__ == "__main__":
    main()

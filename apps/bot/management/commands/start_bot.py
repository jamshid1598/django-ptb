from django.conf import settings
from django.core.management.base import BaseCommand
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hello! Welcome to the bot.')

async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Help!')


async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(update.message.text)


def main() -> None:
    token = settings.BOT_TOKEN
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


class Command(BaseCommand):
    help = 'Starts the Telegram bot'

    def handle(self, *args, **kwargs):
        main()

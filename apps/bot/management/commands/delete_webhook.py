import asyncio
from django.conf import settings
from django.core.management.base import BaseCommand
from telegram.ext import Application


async def delete_webhook():
    token = settings.BOT_TOKEN
    application = Application.builder().token(token).build()
    is_appointed = await application.bot.delete_webhook()
    return is_appointed


class Command(BaseCommand):
    help = 'Delete telegram bot webhook'

    def handle(self, *args, **kwargs):
        is_appointed = asyncio.run(delete_webhook())
        if is_appointed:
            self.stdout.write(self.style.SUCCESS("Webhook was successfully deleted."))
        else:
            self.stdout.write(self.style.ERROR("Something went wrong."))

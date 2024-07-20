import requests
import asyncio
from django.urls import reverse
from django.conf import settings
from django.core.management.base import BaseCommand
from telegram import Update
from telegram.ext import Application


async def set_webhook(token, url):
    application = Application.builder().token(token).build()
    await application.bot.set_webhook(url=url, allowed_updates=Update.ALL_TYPES)


class Command(BaseCommand):
    help = 'Starts the Telegram bot'

    def handle(self, *args, **kwargs):
        domain = settings.SERVER_DOMAIN
        token = settings.BOT_TOKEN
        webhook_url = "https://{}{}".format(domain, reverse("bot:webhook"))

        asyncio.run(set_webhook(token, webhook_url))

        try:
            requests.get(f'https://api.telegram.org/bot{token}/setWebhook?url={webhook_url}')
            self.stdout.write(self.style.SUCCESS("Webhook was successfully appointed."))
        except Exception as e:
            print("Error: ", e)
            self.stdout.write(self.style.ERROR("Something went wrong."))

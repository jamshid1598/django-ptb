import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext


async def start(update: Update, context: CallbackContext) -> None:
    print("Start command")
    await update.message.reply_text('Hello! Welcome to the bot.')


async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Help!')


@csrf_exempt
async def webhook(request):
    token = settings.BOT_TOKEN
    application = Application.builder().token(token).build()
    if request.method == "POST":
        data = json.loads(request.body)
        update = Update.de_json(data, application.bot)

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))

        await application.update_queue.put(update)
        async with application:
            await application.start()
            await application.stop()
        return JsonResponse({"status": "ok"})
    else:
        return JsonResponse({"status": "invalid method"}, status=405)

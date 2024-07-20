import json
import html
import logging
import traceback
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core.exceptions import PermissionDenied, BadRequest
from django.template.loader import render_to_string
from telegram import Update
from telegram.ext import CallbackContext

from apps.bot.tg_init import telegram_bot

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        print("Error: \n\n", exception)
        if exception:
            bot = telegram_bot()
            message = "{url}\n\n{error}".format(
                url=request.build_absolute_uri(),
                error=repr(exception)
            )
            try:
                bot.send_message(
                    text=message,
                    chat_id=settings.BOT_DEVELOPER_CHAT_ID,
                    parse_mode='HTML'
                )
            except Exception:
                pass

        if isinstance(exception, BadRequest):
            rendered = render_to_string("errors/400.html")
            return HttpResponse(rendered, status=400)
        elif isinstance(exception, Http404):
            rendered = render_to_string('errors/404.html')
            return HttpResponse(rendered, status=404)
        elif isinstance(exception, PermissionDenied):
            rendered = render_to_string('errors/403.html')
            return HttpResponse(rendered, status=403)
        rendered = render_to_string('errors/500.html')
        return HttpResponse(rendered, status=500)


def error_handler(update: object, context: CallbackContext) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f'An exception was raised while handling an update\n'
        f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}'
        '</pre>\n\n'
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
        f'<pre>{html.escape(tb_string)}</pre>'
    )

    # Finally, send the message
    msg_list = [message]
    if len(message) > 1000:
        msg_list = [message[:1000], message[1000:]]
    for text in msg_list:
        send_message_to_admin(text)


def send_message_to_admin(message):
    bot = telegram_bot()
    try:
        bot.send_message(
            chat_id=settings.BOT_DEVELOPER_CHAT_ID,
            text=message,
            parse_mode='HTML'
        )
    except Exception as e:
        logger.error("Error on sending message to admin: %" % str(e))


def get_message(request, exception="server error"):
    message = "%s\n\n<pre>%s</pre>" % (
        request.build_absolute_uri(),
        html.escape(json.dumps(repr(exception), indent=2, ensure_ascii=False))
    )
    return message


def error_400(request, exception):
    message = get_message(request, exception)
    send_message_to_admin(message)
    return render(request, 'errors/400.html', status=400)


def error_403(request, exception):
    message = get_message(request, exception)
    send_message_to_admin(message)
    return render(request, 'errors/403.html', status=403)


def error_404(request, exception):
    message = get_message(request, exception)
    send_message_to_admin(message)
    return render(request, 'errors/404.html', status=404)


def error_500(request, *args, **kwargs):
    message = get_message(request)
    send_message_to_admin(message)
    return render(request, 'errors/500.html', status=500)

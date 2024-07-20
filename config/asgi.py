"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
import dotenv
from pathlib import Path
from django.core.asgi import get_asgi_application

base_dir = Path(__file__).resolve().parent.parent
dotenv.read_dotenv(os.path.join(base_dir, '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()

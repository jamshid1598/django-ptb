import os
import dotenv
from pathlib import Path
from django.core.wsgi import get_wsgi_application

base_dir = Path(__file__).resolve().parent.parent
dotenv.read_dotenv(os.path.join(base_dir, '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

from .base import *


DEBUG = True

ALLOWED_HOSTS = []

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

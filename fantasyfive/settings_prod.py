import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('USERNAME', '') + '$' + 'ffl',
        'USER': os.getenv('USERNAME', ''),
        'PASSWORD': os.getenv('MYSQL_PASSWORD', ''),
        'HOST': os.getenv('MYSQL_HOSTNAME', ''),
        'PORT': ''
    }
}
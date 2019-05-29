from .searchengine import BaseSearchEngine
from django.conf import settings


if 'django.contrib.postgres' not in settings.INSTALLED_APPS:
    settings.INSTALLED_APPS.append('django.contrib.postgres')


class TrigramSearchEngine(BaseSearchEngine):
    pass

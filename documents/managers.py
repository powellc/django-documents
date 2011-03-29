from django.db import models
from datetime import datetime

class PublishedManager(models.Manager):
    def get_query_set(self):
        return super(PublishedManager, self).get_query_set().filter(published=True, published_on__lte=datetime.now())

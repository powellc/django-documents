from django.contrib.syndication.views import Feed
from documents.models import Document
from django.conf import settings
from django.contrib.sites.models import Site

class LatestDocumentsFeed(Feed):
    current_site = Site.objects.get(id=settings.SITE_ID)
    title = current_site.name + " documents"
    link = current_site.domain
    item_copyright="Copyright (r) 2010, Penobscot Bay Press"

    description = "Documents recently published by Penobscot Bay Press"
    
    def items(self):
        return Document.published_objects.all()[:30]
    
    def item_pubdate(self, item):
        return item.published_on

    def item_title(self, item):
        return item.title
    
    def item_link(self, item):
        return item.get_absolute_url()

    def item_description(self, item):
        return item.description


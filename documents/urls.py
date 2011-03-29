from django.conf import settings
from django.conf.urls.defaults import *
from documents.models import *
from documents import views as dc_views
from documents.feeds import LatestDocumentsFeed

# custom views stories
urlpatterns = patterns('documents.views',
    url(r'^$', view=dc_views.index, name="dc-index"),
    url(r'^feed.xml', LatestDocumentsFeed(), name="dc-feed"),
    # We use a custom view so we can increment the view_count
    url(r'(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$', view=dc_views.document_detail, name='dc-document-detail'),
    url(r'(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$', view=dc_views.document_detail, name='dc-pdf-document-detail'),
)
doc_args = {'date_field': 'published_on', 'queryset': Document.published_objects.all()}

urlpatterns += patterns('django.views.generic.date_based',
    url(r'(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 'archive_day', doc_args, name='dc-document-archive-day'),
    url(r'(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'archive_month', doc_args, name='dc-document-archive-month'),
    url(r'(?P<year>\d{4})/$', 'archive_year', doc_args, name='dc-document-archive-year'),
)

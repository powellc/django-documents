from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic.list_detail import object_list
from django.template.context import RequestContext

from documents.models import Document 

def index(request):
    objects=Document.published_objects.all()
    return render_to_response('documents/index.html', locals(),
                              context_instance=RequestContext(request))

def document_detail(request, year, month, day, slug):
    object=get_object_or_404(Document, slug=slug)
    return render_to_response('documents/document_detail.html', locals(),
                              context_instance=RequestContext(request))

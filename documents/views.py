from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list

from documents.models import DocumentAttachedItem, Document 

def document_attached_object_list(request, slug, queryset, **kwargs):
    if callable(queryset):
        queryset = queryset()
    document = get_object_or_404(Document, slug=slug)
    qs = queryset.filter(pk__in=DocumentAttachedItem.objects.filter(
        document=document, content_type=ContentType.objects.get_for_model(queryset.model)
    ).values_list("object_id", flat=True))
    if "extra_context" not in kwargs:
        kwargs["extra_context"] = {}
    kwargs["extra_context"]["document"] = document 
    return object_list(request, qs, **kwargs)


from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.db import models, IntegrityError, transaction
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _, ugettext

from directory.models import Place
from taggit.managers import TaggableManager
from django_extensions.db.models import TimeStampedModel
from documents.managers import PublishedManager

class Document(TimeStampedModel):
    ACCESS_CHOICES = (('public', 'Public'),
                     ('private', 'Private'),
                     ('organization', 'Organization'))
    title = models.CharField(verbose_name=_('Title'), max_length=255)
    slug = models.SlugField(verbose_name=_('Slug'), unique=True, max_length=200)
    description=models.TextField(_('Description'), blank=True, null=True )
    source=models.CharField(_('Source'), max_length=100)
    access=models.CharField(_('Access'), max_length=12, choices=ACCESS_CHOICES, default='public')
    published=models.BooleanField(_('published'), default=False)
    published_on=models.DateTimeField(_('published on'))
    preview=models.ImageField(_('preview'), upload_to="documents/previews", blank=True, null=True)
    doc_cloud_id=models.SlugField(max_length=80, editable=False, null=True, blank=True)

    tags = TaggableManager()
    objects=models.Manager()
    published_objects=PublishedManager()

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")

    @models.permalink 
    def get_absolute_url(self):
        return ('dc-document-detail', (), {
                'year': self.published_on.year,
                'month': self.published_on.strftime('%b').lower(),
                'day': self.published_on.day,
                'slug': self.slug})

    @property
    def display(self):
        return True

class TextDocument(Document):
    content=models.TextField(_('content'), blank=True, null=True, help_text="If document is plaintext, insert it here.")

    class Meta:
        verbose_name = _("Text Document")
        verbose_name_plural = _("Text Documents")

    @models.permalink 
    def get_absolute_url(self):
        return ('dc-text-document-detail', (), {
                'year': self.published_on.year,
                'month': self.published_on.strftime('%b').lower(),
                'day': self.published_on.day,
                'slug': self.slug})

class PDFDocument(Document):
    file=models.FileField(_('file'), upload_to="documents/pdf/%Y/%b/%d")

    class Meta:
        verbose_name = _("PDF Document")
        verbose_name_plural = _("PDF Documents")

    @models.permalink 
    def get_absolute_url(self):
        return ('dc-pdf-document-detail', (), {
                'year': self.published_on.year,
                'month': self.published_on.strftime('%b').lower(),
                'day': self.published_on.day,
                'slug': self.slug})

class ExcelDocument(Document):
    file=models.FileField(_('file'), upload_to="documents/excel/%Y/%b/%d")

    class Meta:
        verbose_name = _("Excel Document")
        verbose_name_plural = _("Excel Documents")

    @models.permalink 
    def get_absolute_url(self):
        return ('dc-xcl-document-detail', (), {
                'year': self.published_on.year,
                'month': self.published_on.strftime('%b').lower(),
                'day': self.published_on.day,
                'slug': self.slug})

class WordDocument(Document):
    file=models.FileField(_('file'), upload_to="documents/word/%Y/%b/%d")

    class Meta:
        verbose_name = _("Word Document")
        verbose_name_plural = _("Word Documents")

    @models.permalink 
    def get_absolute_url(self):
        return ('dc-word-document-detail', (), {
                'year': self.published_on.year,
                'month': self.published_on.strftime('%b').lower(),
                'day': self.published_on.day,
                'slug': self.slug})

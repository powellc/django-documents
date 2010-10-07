import django
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.db import models, IntegrityError, transaction
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _, ugettext


class DocumentBase(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=255)
    slug = models.SlugField(verbose_name=_('Slug'), unique=True, max_length=200)
    summary=models.TextField(_('summary') )
    file=models.FileField(_('file'), upload_to=NEWSROOM_DIR+"/documents/%Y/%b/%d")
    content=models.TextField(_('content'), blank=True, null=True, help_text="If document is plaintext, insert it here.")
    source=models.ForeignKey(Place, blank=True, null=True, help_text="Source of document.")
    published=models.BooleanField(_('published'), default=False)
    published_on=models.DateTimeField(_('published on'))
    preview=models.ImageField(_('preview'), upload_to=NEWSROOM_DIR+"/documents/previews", blank=True, null=True)

    tags = TaggableManager()



    def __unicode__(self):
        return self.title

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk and not self.slug:
            self.slug = slug = slugify(self.name)
            if django.VERSION >= (1, 2):
                from django.db import router
                using = kwargs.get("using") or router.db_for_write(
                    type(self), instance=self)
                # Make sure we write to the same db for all attempted writes,
                # with a multi-master setup, theoretically we could try to
                # write and rollback on different DBs
                kwargs["using"] = using
                trans_kwargs = {"using": using}
            else:
                trans_kwargs = {}
            i = 0
            while True:
                try:
                    sid = transaction.savepoint(**trans_kwargs)
                    res = super(TagBase, self).save(*args, **kwargs)
                    transaction.savepoint_commit(sid, **trans_kwargs)
                    return res
                except IntegrityError:
                    transaction.savepoint_rollback(sid, **trans_kwargs)
                    i += 1
                    self.slug = "%s_%d" % (slug, i)
        else:
            return super(DocumentBase, self).save(*args, **kwargs)

class Document(DocumentBase):
    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")

    @models.permalink
    def get_absolute_url(self):
        return ('document_detail', (), {'year': self.published_on.year, 'slug': self.slug})

class ItemBase(models.Model):
	def __unicode__(self):
		return ugettext("%(object)s with %(document) attached") % {
			"object": self.content_object,
			"document": self.document
		}

	class Meta:
		abstract = True

	@classmethod
	def document_model(cls):
		return cls._meta.get_field_by_name("document")[0].rel.to

	@classmethod
	def document_relname(cls):
		return cls._meta.get_field_by_name('document')[0].rel.related_name

	@classmethod
	def lookup_kwargs(cls, instance):
		return {
			'content_object': instance
		}

class DocumentAttachedItemBase(ItemBase):
	if django.VERSION < (1, 2):
		document = models.ForeignKey(Document, related_name="%(class)s_with_documents")
	else:
		document = models.ForeignKey(Document, related_name="%(app_label)s_%(class)s_with_documents")

	class Meta:
		abstract = True

	@classmethod
	def documents_for(cls, model, instance=None):
		if instance is not None:
			return cls.document_model().objects.filter(**{
				'%s__content_object' % cls.tag_relname(): instance
			})
		return cls.document_model().objects.filter(**{
			'%s__content_object__isnull' % cls.document.relname(): False
		}).distinct()

class GenericDocumentAttachedItemBase(ItemBase):
	object_id = models.IntegerField(verbose_name=_('Object ID'), db_index=True)
	if django.VERSION < (1, 2):
		content_type = models.ForeignKey(
				ContentType,
				verbose_name=_('Content type'),
				related_name="%(class)s_attached_items"
		)
	else:
		content_type = models.ForeignKey(
				ContentType,
				verbose_name=_('Content type'),
				related_name="%(app_label)s_%(class)s_with_documents"
		)
	content_object = GenericForeignKey()

	class Meta:
		abstract = True
	
	@classmethod
	def lookup_kwargs(cls, instance):
		return {
			'object_id': instance.pk,
			'content_type': ContentType.objects.get_for_model(instance)
		}

	@classmethod
	def documents_for(cls, model, instance=None):
		ct = ContentType.objects.get_for_model(model)
		kwargs = {
				"%s__content_type" % cls.document_relname(): ct
		}
		if instance is not None:
			kwargs["%s__object_id" % cls.document_relname()] = instance.pk
		return cls.document_model().objects.filter(**kwargs).distinct()

class ItemWithDocuments(GenericDocumentAttachedItemBase, DocumentAttachedItemBase):
	class Meta:
		verbose_name = _("Item with Documents")
		verbose_name_plural = _("Items with Documents")

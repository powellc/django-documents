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


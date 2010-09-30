Django Documents
================

A reusable application to allow uploading documents and attaching them to whatever
model you wish. Most of the code is really just taken from Gaynor's taggit app.

Usage
-----

1. Add "documents" to your INSTALLED_APPS
2. Add the following to your project urls.py file:
   (r'^documents/', include('documents.urls')),
3. If you want to attach documents to your class, in your models definition add:
   
    class Horse(AnimalModel):
      model fields here...
      ...

      documents = AttachedDocumentManager()

Then you can access documents like so:

    >>> the_book=Document.objects.get(title="Black Beauty, the Book")
    >>> black_beauty = Horse.objects.create(name="Black Beauty")
    >>> black_beauty.documents.add(the_book)
    >>> black_beauty.tags.all()
    [<Document: black-beauty-the-book>]
    >>> black_beauty.documents.remove(the_book)
    >>> black_beauty.documents.all()
    []
    >>> Horse.objects.filter(documents__slug__in=["black-beauty-the-book"])
    [<Horse: black-beauty>]

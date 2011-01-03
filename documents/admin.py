from django.contrib import admin 
from documents.models import *

#admin.site.register(Document)
admin.site.register(TextDocument)
admin.site.register(PDFDocument)
admin.site.register(WordDocument)
admin.site.register(ExcelDocument)

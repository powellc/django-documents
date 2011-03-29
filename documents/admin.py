from django.contrib import admin 
from documents.models import *
'''
class PDFDocAdmin(admin.ModelAdmin):
    prepopulated_fields={"slug": ("title",)}
    list_display = ('type', 'name', 'created', 'user',)
'''

#admin.site.register(Document)
admin.site.register(TextDocument)
admin.site.register(PDFDocument)
admin.site.register(WordDocument)
admin.site.register(ExcelDocument)

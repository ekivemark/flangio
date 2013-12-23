from django.contrib import admin
from models import Transaction, DataLabelMeta

admin.site.register(Transaction)



class DataLabelMetaAdmin(admin.ModelAdmin):

    list_display = ('variable_name','verbose_name', 'label', 'question_text')
    search_fields = ('variable_name', 'verbose_name', 'label', 'question_text')

admin.site.register(DataLabelMeta, DataLabelMetaAdmin)
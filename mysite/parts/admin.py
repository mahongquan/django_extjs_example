from django.contrib import admin
from mysite.parts.models import *
class ContactItemInline(admin.TabularInline):
    model=ContactItem
class ContactAdmin(admin.ModelAdmin):
    inlines=[ContactItemInline,]
admin.site.register(Contact,ContactAdmin)
admin.site.register(ContactItem)
admin.site.register(Item)

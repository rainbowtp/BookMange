from django.contrib import admin

# Register your models here.
from .models import *


class PulishAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Publish, PulishAdmin)


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'publish')


admin.site.register(Book, BookAdmin)

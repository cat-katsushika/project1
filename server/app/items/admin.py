from django.contrib import admin

from .models import Image, Item, Like


class ImageInline(admin.TabularInline):
    model = Image


class ItemAdmin(admin.ModelAdmin):
    inlines = [ImageInline]


admin.site.register(Item, ItemAdmin)
admin.site.register(Like)

from django.contrib import admin

from .models import Image, Item


class ImageInline(admin.TabularInline):
    model = Image


class ItemAdmin(admin.ModelAdmin):
    inlines = [ImageInline]


admin.site.register(Item, ItemAdmin)

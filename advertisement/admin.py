from django.contrib import admin
from .models import Advertisement, AdvertisementImage


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'user',)
    list_filter = ('title', 'user',)
    search_fields = ('title',)
    ordering = ('title',)


class AdvertisementImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'advertisement',)
    list_filter = ('image', 'advertisement',)
    search_fields = ('advertisement',)


admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(AdvertisementImage, AdvertisementImageAdmin)

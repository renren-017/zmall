from django.contrib import admin
from .models import Advertisement, AdvertisementImage, Category, SubCategory

# class AdvertisementAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'user',)
#     list_filter = ('id', 'title', 'user',)
#     search_fields = ('id', 'title',)
#     ordering = ('-id', )


# class AdvertisementImageAdmin(admin.ModelAdmin):
#     list_display = ('id', 'image', 'advertisement',)
#     list_filter = ('id', 'image', 'advertisement',)
#     search_fields = ('advertisement',)
#     ordering = ('-id', )


admin.site.register(Advertisement)
admin.site.register(AdvertisementImage)
admin.site.register(Category)
admin.site.register(SubCategory)

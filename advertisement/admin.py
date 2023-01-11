from django.contrib import admin
from .models import Advertisement, AdvertisementImage, Category, SubCategory, AdvertisementPromotion, Promotion


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('id', 'sub_category', 'title', 'owner', 'description', 'city', 'views', 'created_on')
    list_filter = ('id', 'title', 'owner')
    search_fields = ('id', 'title',)
    ordering = ('-created_on',)


# class AdvertisementImageAdmin(admin.ModelAdmin):
#     list_display = ('id', 'image', 'advertisement',)
#     list_filter = ('id', 'image', 'advertisement',)
#     search_fields = ('advertisement',)
#     ordering = ('-id', )


admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(AdvertisementImage)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(AdvertisementPromotion)
admin.site.register(Promotion)

from django.db import models
from django.utils.text import slugify

from user.models import CustomUser
# from cities.models import BaseCountry


def get_upload_path_ad_image(instance, filename):
    return "ad_images/{username}/{file}".format(username=instance.advertisement.username(), file=filename)


def get_upload_path_head_image(instance, filename):
    return "ad_images/{username}/{file}".format(username=instance.username(), file=filename)


class Category(models.Model):
    # slug = models.SlugField(max_length=150, unique=True, blank=True)
    title = models.CharField(max_length=50)


class SubCategory(models.Model):
    # slug = models.SlugField(max_length=150, unique=True, blank=True)
    title = models.CharField(max_length=50)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name='sub_category')


class Advertisement(models.Model):

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    sub_category = models.ForeignKey(to=SubCategory, on_delete=models.DO_NOTHING, related_name='advertisement')
    price = models.PositiveIntegerField(default=0)
    max_price = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0, blank=True)
    city = models.CharField(max_length=150)
    end_date = models.DateTimeField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def username(self):
        return self.user.username

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Promotion(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()


class AdvertisementPromotion(models.Model):
    # advertisement = models.ForeignKey(Advertisement, on_delete=models.PROTECT, related_name='promotion')
    promotion = models.ForeignKey(to=Promotion, on_delete=models.CASCADE, related_name='sub_promotion')


class AdvertisementImage(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='images')
    image = models.FileField(upload_to=get_upload_path_ad_image, blank=True, null=True)


class AdvertisementComment(models.Model):
    parent_id = models.IntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()





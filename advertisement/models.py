from django.db import models
from user.models import CustomUser
from cities.models import BaseCountry


def get_upload_path_ad_image(instance, filename):
    return "ad_images/{username}/{file}".format(username=instance.advertisement.username(), file=filename)


def get_upload_path_head_image(instance, filename):
    return "ad_images/{username}/{file}".format(username=instance.username(), file=filename)


class Category(models.Model):
    title = models.CharField(max_length=50)


class SubCategory(models.Model):
    title = models.CharField(max_length=50)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name='sub_category')


class Advertisement(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField()
    head_image = models.FileField(upload_to=get_upload_path_head_image, blank=True, null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    max_price = models.PositiveIntegerField()
    views = models.PositiveIntegerField()
    city = BaseCountry()
    end_date = models.DateTimeField()
    created_on = models.DateTimeField()

    def username(self):
        return self.user.username

    def __str__(self):
        return self.title


class AdvertisementImage(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    image = models.FileField(upload_to=get_upload_path_ad_image, blank=True, null=True)


class AdvertisementComment(models.Model):
    parent_id = models.IntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()


class AdvertisementPromotion(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='promotion')


class Promotion(models.Model):
    name = models.CharField()
    price = models.FloatField()
    advertisement_promotion = models.ForeignKey(AdvertisementPromotion,
                                                on_delete=models.CASCADE,
                                                related_name='promotion')

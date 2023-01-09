from django.contrib.auth import get_user_model
from rest_framework import serializers
from advertisement.models import Advertisement, Category, SubCategory, AdvertisementImage, AdvertisementComment, \
    AdvertisementPromotion, Promotion
from django.utils import timezone

User = get_user_model()


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ['id', 'name', 'price']


class AdvertisementPromotionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdvertisementPromotion
        fields = ['id', 'promotion']


class AdvertisementCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementComment
        fields = ['id', ]


class AdvertisementImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementImage
        fields = ['id', 'image', 'advertisement']

    def create(self, validated_data):
        advertisement = Advertisement.objects.get(pk=validated_data['advertisement'])
        image = AdvertisementImage(
            image=validated_data['image'],
            advertisement=advertisement
        )
        image.save()
        return image

    def update(self, instance, validated_data):
        return AdvertisementImageSerializer(**validated_data).save()


class AdvertisementSerializer(serializers.ModelSerializer):
    views = serializers.IntegerField(read_only=True)
    created_on = serializers.DateTimeField(read_only=True)
    images = AdvertisementImageSerializer(many=True, read_only=True)
    comments = AdvertisementCommentSerializer(many=True, read_only=True)
    # promotion = AdvertisementPromotionSerializer(many=True, read_only=True)

    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'description', 'sub_category', 'price',
                  'max_price', 'views', 'city', 'end_date', 'created_on', 'images', 'comments']

    def create(self, validated_data):
        owner = User.objects.get(pk=1)
        obj = Advertisement(
            owner=owner,
            title=validated_data['title'],
            description=validated_data['description'],
            sub_category=validated_data['sub_category'],
            price=validated_data.get('price', 0),
            max_price=validated_data.get('max_price', 0),
            city=validated_data['city'],
            end_date=validated_data.get('end_date', timezone.now()),
        )
        obj.save()
        return obj

    def update(self, instance, validated_data):
        return AdvertisementSerializer(**validated_data).save()


class SubCategorySerializer(serializers.ModelSerializer):
    advertisements = AdvertisementSerializer(many=True, read_only=True)

    class Meta:
        model = SubCategory
        fields = ('id', 'category', 'title', "advertisements")


class CategorySerializer(serializers.ModelSerializer):
    sub_category = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'title', 'sub_category')




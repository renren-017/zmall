from rest_framework import serializers
from advertisement.models import Advertisement, Category, SubCategory, AdvertisementImage, AdvertisementComment, \
    AdvertisementPromotion, Promotion


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ['id', 'name']


class AdvertisementPromotionSerializer(serializers.ModelSerializer):
    promotion = PromotionSerializer(many=True, read_only=True)

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
        image = AdvertisementImage(
            image=validated_data['image'],
            advertisement=validated_data['advertisement']
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
                  'max_price', 'views', 'city', 'end_date', 'created_on', 'images', 'comments', 'promotion']

    def update(self, instance, validated_data):
        return AdvertisementSerializer(**validated_data).save()


class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = ('id', 'slug', 'title')


class CategorySerializer(serializers.ModelSerializer):
    sub_category = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'title', 'sub_category')




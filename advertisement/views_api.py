from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import RetrieveAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView, \
    RetrieveUpdateDestroyAPIView, CreateAPIView, DestroyAPIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.pagination import LimitOffsetPagination

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.views import APIView

from core.db_management.queries import get_ads_filtered
from advertisement.models import Advertisement, Category, SubCategory, Promotion, AdvertisementPromotion, \
    AdvertisementImage, Favorite
from advertisement.serializers import AdvertisementSerializer, CategorySerializer, SubCategorySerializer, \
    PromotionSerializer, AdvertisementPromotionSerializer, AdvertisementImageSerializer, FavoriteSerializer
from user.models import CustomUser


class AdvertisementListView(ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = (SearchFilter, )
    serializer_class = AdvertisementSerializer
    pagination_class = LimitOffsetPagination
    search_fields = ('title', 'description')
    queryset = Advertisement.objects.select_related('sub_category').all()

    def get_queryset(self):
        queryset = Advertisement.objects.all()
        price = self.request.query_params.get('price')
        max_price = self.request.query_params.get('max_price')
        city = self.request.query_params.get('city')
        has_image = self.request.query_params.get('has_image')

        if any([price, max_price, city, has_image]):
            queryset = get_ads_filtered(price=price, max_price=max_price, city=city, has_image=has_image)
        return queryset

    price = openapi.Parameter('price', openapi.IN_QUERY,
                              type=openapi.TYPE_NUMBER)
    max_price = openapi.Parameter('max_price', openapi.IN_QUERY,
                                  type=openapi.TYPE_NUMBER)
    city = openapi.Parameter('city', openapi.IN_QUERY,
                             type=openapi.TYPE_STRING)
    has_image = openapi.Parameter('has_image', openapi.IN_QUERY,
                                  type=openapi.TYPE_BOOLEAN)

    @swagger_auto_schema(manual_parameters=[price, max_price, city, has_image])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class AdvertisementImageAPIView(CreateAPIView):
    model = AdvertisementImage
    serializer_class = AdvertisementImageSerializer
    parser_classes = (MultiPartParser, FormParser)


class AdvertisementDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Advertisement.objects.all()
    model = Advertisement
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = AdvertisementSerializer


class CategoryListAPIView(ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    model = Category
    queryset = Category.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = (SearchFilter, )
    serializer_class = CategorySerializer


class CategoryDetailAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Category.objects.all()
    parser_classes = (JSONParser, )
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class SubCategoryListAPIView(ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    model = SubCategory
    queryset = SubCategory.objects.select_related('category').all()
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = (SearchFilter, )
    serializer_class = SubCategorySerializer


class SubCategoryDetailAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = SubCategory.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = SubCategorySerializer
    lookup_field = 'slug'


class PromotionListAPIView(ListAPIView):
    queryset = Promotion.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = (SearchFilter, )
    serializer_class = PromotionSerializer


class PromotionDetailAPIView(RetrieveAPIView):
    model = Promotion
    queryset = Promotion.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = PromotionSerializer


class AdvertisementPromotionListAPIView(ListAPIView):
    model = AdvertisementPromotion
    queryset = AdvertisementPromotion.objects.prefetch_related('advertisement').all()
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = AdvertisementPromotionSerializer
    filter_backends = (SearchFilter, )


class AdvertisementPromotionDetailAPIView(RetrieveAPIView):
    model = AdvertisementPromotion
    queryset = AdvertisementPromotion.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = AdvertisementPromotionSerializer


class AdvertisementFavoriteAPIView(ListCreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated, )
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteDeleteAPIView(DestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(request_body=FavoriteSerializer,
                         operation_summary='Removes advertisement from favorites')
    def delete(self, request, *args, **kwargs):
        user = self.request.user
        queryset = Favorite.objects.filter(user=user, advertisement_id=request.data['advertisement'])
        if queryset.exists():
            queryset.delete()
            return Response('Deleted', status=status.HTTP_204_NO_CONTENT)
        return Response('Advertisement does not exist in favorite', status=status.HTTP_404_NOT_FOUND)

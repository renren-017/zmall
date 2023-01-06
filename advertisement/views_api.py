from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, RetrieveDestroyAPIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api_auth.backends import JWTAuthentication
from advertisement.models import Advertisement, Category, SubCategory, Promotion, AdvertisementPromotion, \
    AdvertisementImage
from advertisement.serializers import AdvertisementSerializer, CategorySerializer, SubCategorySerializer, \
    PromotionSerializer, AdvertisementPromotionSerializer, AdvertisementImageSerializer


class AdvertisementListView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Advertisement.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = (SearchFilter, )
    serializer_class = AdvertisementSerializer


class AdvertisementDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'slug'
    queryset = Advertisement.objects.all()
    model = Advertisement
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = AdvertisementSerializer


class CategoryListAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    model = Category
    queryset = Category.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = (SearchFilter, )
    serializer_class = CategorySerializer


class CategoryDetailAPIView(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Category.objects.all()
    parser_classes = (JSONParser, )
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class SubCategoryListAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    model = SubCategory
    queryset = SubCategory.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = (SearchFilter, )
    serializer_class = SubCategorySerializer


class SubCategoryDetailAPIView(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = SubCategory.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = SubCategorySerializer
    lookup_field = 'slug'


class PromotionListAPIView(ListCreateAPIView):
    queryset = Promotion.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = (SearchFilter, )
    serializer_class = PromotionSerializer


class PromotionDetailAPIView(RetrieveUpdateDestroyAPIView):
    model = Promotion
    queryset = Promotion.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = PromotionSerializer


class AdvertisementPromotionListAPIView(ListCreateAPIView):
    model = AdvertisementPromotion
    queryset = AdvertisementPromotion.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = AdvertisementPromotionSerializer
    filter_backends = (SearchFilter, )


class AdvertisementPromotionDetailAPIView(RetrieveUpdateDestroyAPIView):
    model = AdvertisementPromotion
    queryset = AdvertisementPromotion.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = AdvertisementPromotionSerializer


class AdvertisementImageAPIView(APIView):
    model = AdvertisementImage
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(operation_summary='Creates a new image', request_body=AdvertisementImageSerializer)
    def post(self, request, *args, **kwargs):
        serializer = AdvertisementImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UpdateImageAPIView(RetrieveUpdateDestroyAPIView):
    model = AdvertisementImage
    queryset = AdvertisementImage.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = AdvertisementImageSerializer

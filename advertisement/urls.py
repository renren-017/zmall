from django.urls import path
from . import views
from .views_api import *

urlpatterns = [
    path('create/', views.create_ad_view, name='create_ad'),
    path('advertisement/', AdvertisementListView.as_view(), name='advertisement-list'),
    path('advertisement/<slug:slug>', AdvertisementDetailAPIView.as_view(), name='advertisement-detail'),
    path('advertisement/add_image', AdvertisementImageAPIView.as_view(), name='add-image'),
    path('image/<int:pk>', UpdateImageAPIView.as_view()),
    path('category/', CategoryListAPIView.as_view()),
    path('category/<slug:slug>', CategoryDetailAPIView.as_view()),
    path('sub-category/', SubCategoryListAPIView.as_view()),
    path('sub-category/<slug:slug>', SubCategoryDetailAPIView.as_view()),
    path('promotion/', PromotionListAPIView.as_view()),
    path('promotion/<int:pk>', PromotionDetailAPIView.as_view()),
    path('sub-promotion/', AdvertisementPromotionListAPIView.as_view()),
    path('sub-promotion/<int:pk>', AdvertisementPromotionDetailAPIView.as_view()),
]

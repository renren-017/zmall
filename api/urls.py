from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterApi.as_view(), name='api-register'),
    path('api/token/', views.TokenObtainView.as_view(), name='api-token-obtain'),
    path('api/token/refresh', views.TokenRefreshView.as_view(), name='api-token-refresh')
]

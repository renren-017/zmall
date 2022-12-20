from django.urls import path
from api_auth import views

urlpatterns = [
    path('register/', views.RegisterApi.as_view(), name='api-register'),
    path('token/', views.TokenObtainView.as_view(), name='api-token-obtain'),
    path('token/refresh/', views.TokenRefreshView.as_view(), name='api-token-refresh')
]

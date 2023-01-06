from django.urls import path, re_path
from api_auth import views

urlpatterns = [
    path('register/', views.RegisterApi.as_view(), name='api-register'),
    re_path(r'^email-confirm/(?P<key>[-:\w]+)/$', views.EmailVerificationView.as_view(),
            name='api-confirm-email'),
    path('token/', views.TokenObtainView.as_view(), name='api-token-obtain'),
    path('token/refresh/', views.TokenRefreshView.as_view(), name='api-token-refresh')
]

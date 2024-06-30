from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import PaymentListAPIView, UserCreateAPIView, UserUpdateAPIView, UserListAPIView, UserRetrieveAPIView, \
    UserDestroyAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='create_user'),
    path('edit/<int:pk>/', UserUpdateAPIView.as_view(), name='edit_user'),
    path('', UserListAPIView.as_view(), name='users'),
    path('profile/<int:pk>/', UserRetrieveAPIView.as_view(), name='user'),
    path('delete/<int:pk>/', UserDestroyAPIView.as_view(), name='delete_user'),
    # payments
    path('payments/', PaymentListAPIView.as_view(), name='payments'),
    # token
    path('token/', TokenObtainPairView.as_view(permission_classes=[AllowAny]), name='create_token'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=[AllowAny]), name='refresh_token'),
]

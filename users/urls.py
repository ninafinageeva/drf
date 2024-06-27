from django.urls import path
from rest_framework.routers import DefaultRouter

from users.apps import UsersConfig
from users.views import UserViewSet, PaymentListAPIView

app_name = UsersConfig.name
router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
urlpatterns = [
                  path('payments/', PaymentListAPIView.as_view(), name='payments_list'),
              ] + router.urls

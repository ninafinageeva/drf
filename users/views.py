from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User, Payment
from users.permissions import IsUser
from users.serializers import UserSerializer, PaymentSerializer, UserViewSerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """Хеширование пароля"""
        instance = serializer.save(is_active=True)
        instance.set_password(instance.password)
        instance.save()


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsUser]

    def perform_update(self, serializer):
        """Хеширование пароля при редактировании"""
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserViewSerializer


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        """Проверка на владельца профиля"""
        if self.request.user.email == self.get_object().email:
            return UserSerializer
        else:
            return UserViewSerializer


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()


# class UserViewSet(ModelViewSet):
#     """Реализация через ViewSet"""
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')
    ordering_fields = ('payment_date',)


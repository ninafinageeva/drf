from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from materials.permissions import IsModerator, IsOwner

from materials.models import Course, Lesson, Subscription
from materials.paginators import CustomPaginator
from materials.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer

@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="description from swagger_auto_schema via method_decorator"
))  # тестовое значение для кастомизации документации
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPaginator

    def perform_create(self, serializer):
        """Привязывает курс к пользователю при создании"""
        instance = serializer.save()
        instance.owner = self.request.user
        instance.save()

    def get_permissions(self):
        """Настройка прав для ViewSet"""
        if self.action in ['update', 'partial_update', 'list', 'retrieve']:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'create':
            self.permission_classes = [~IsModerator, IsAuthenticated]
        elif self.action == 'destroy':
            self.permission_classes = [~IsModerator | IsOwner]
        return super().get_permissions()


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [~IsModerator, IsAuthenticated]

    def perform_create(self, serializer):
        """Привязывает урок к пользователю при создании"""
        instance = serializer.save()
        instance.owner = self.request.user
        instance.save()


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPaginator


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner]


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [~IsModerator | IsOwner]


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

    def post(self, request, *args, **kwargs):
        """ Переопределение метода для создания и удаления подписки в зависимости от её статуса. """
        user = self.request.user
        course_id = self.request.data.get('course')
        course_item = get_object_or_404(Course, pk=course_id)
        # создание и удаление подписки
        subscription, created = Subscription.objects.get_or_create(user=user, course=course_item, is_subscribed=True)
        if not created:
            subscription.delete()
            message = 'подписка удалена'
        else:
            message = 'подписка добавлена'
        return Response({"message": message})


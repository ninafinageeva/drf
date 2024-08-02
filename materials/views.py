from django.utils import timezone
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from materials.permissions import IsModerator, IsOwner

from materials.models import Course, Lesson, Subscription
from materials.paginators import CustomPaginator
from materials.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from materials.tasks import send_updates
from users.models import User


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPaginator

    def perform_create(self, serializer):
        """Привязывает курс к пользователю при создании"""
        instance = serializer.save()
        instance.owner = self.request.user
        instance.save()

    def perform_update(self, serializer):
        """ Запускает send_updates при редактировании курса. """
        serializer.save()
        course = serializer.save()
        course_id = course.id
        send_updates.delay(course_id)

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
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """ Переопределение метода для создания и удаления подписки в зависимости от её статуса. """
        user = self.request.user
        course_id = self.request.data.get('course')
        course = get_object_or_404(Course, pk=course_id)
        # создание и удаление подписки
        if Subscription.objects.filter(user=user, course=course).exists():
            Subscription.objects.filter(user=user, course=course).delete()
            message = f"Подписка для пользователя {user} на курс {course} удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = f"Подписка для пользователя {user} на курс {course} создана"
        return Response({"message": message})

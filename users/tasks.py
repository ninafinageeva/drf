from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def check_last_login():
    """
    Проверяет дату последнего входа пользователя и
    блокирует пользователя в случае отсутсвия более 1 месяца
    """
    tmp_date = timezone.now() - timezone.timedelta(days=30)
    users = User.objects.filter(is_active=True).exclude(is_superuser=True).filter(last_login__lt=tmp_date)
    for user in users:
        user.is_active = False
        user.save()


from celery import shared_task
from datetime import datetime

from users.models import User


@shared_task
def check_user_activity():
    """
    Проверяем активность пользователя, если больше 30 дней, деактивируем
    """
    users = User.objects.all()
    date_now = datetime.date.today()
    deactivate_time = datetime.timedelta(month=1)
    for user in users:
        if date_now - user.last_login > deactivate_time:
            user.is_active = False
            user.save()

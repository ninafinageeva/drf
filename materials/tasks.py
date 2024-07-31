from datetime import datetime

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER


@shared_task
def send_updates(email_list, course):
    """ При обновлении курса отправляет письмо пользователю, подписанному на курс. """
    updated_at = datetime.strftime(timezone.now(), "%d.%m.%Y %H:%M")   # Преобразуем дату в удобный вид
    message = f"Курc {course} обновлен {updated_at}."
    send_mail("Обновление курса", message, EMAIL_HOST_USER, email_list)

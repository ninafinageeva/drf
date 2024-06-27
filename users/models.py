from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    """Модель пользователя"""

    name = None
    email = models.EmailField(
        unique=True, verbose_name="email", help_text="Email address"
    )
    phone = models.CharField(
        max_length=35, verbose_name="телефон", help_text="номер телефона", **NULLABLE
    )
    city = models.CharField(
        max_length=200, verbose_name="город", help_text="ваш город", **NULLABLE
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="аватар",
        help_text="ваш аватар",
        **NULLABLE
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"


class Payment(models.Model):
    """Модель оплаты"""

    METHOD_CHOICES = [
        ("Cash", "Наличные"),
        ("Non-cash", "Безнал"),
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_payment",
        verbose_name="пользователь",
        help_text="выберите пользователя",
        **NULLABLE
    )
    date_of_payment = models.DateTimeField(
        auto_now_add=True,
        verbose_name="дата оплаты",
        **NULLABLE
    )
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="оплаченный курс",
        **NULLABLE
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name="оплаченный урок",
        **NULLABLE
    )
    payment_amount = models.PositiveIntegerField(
        verbose_name="сумма оплаты",
        help_text="введите сумму оплаты",
        **NULLABLE
    )
    payment_method = models.CharField(
        max_length=20,
        choices=METHOD_CHOICES,
        verbose_name="способ оплаты",
        help_text="выберите способ оплаты"
    )

    def __str__(self):
        return f'''{self.user}: {self.date_of_payment}, {self.payment_amount}, {self.payment_method}
{self.paid_course if self.paid_course else self.paid_lesson}'''

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежи"

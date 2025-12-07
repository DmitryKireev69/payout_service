import uuid
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class PayoutClaim(models.Model):
    """
    Модель заявки на выплату средств.
    """

    class Currency(models.TextChoices):
        RUB = 'RUB', 'Российский рубль'
        USD = 'USD', 'Доллар США'
        EUR = 'EUR', 'Евро'
        KZT = 'KZT', 'Казахстанский тенге'
        CNY = 'CNY', 'Китайский юань'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Ожидает обработки'
        PROCESSING = 'processing', 'В обработке'
        PROCESSED = 'processed', 'Обработана'
        REJECTED = 'rejected', 'Отклонена'
        CANCELLED = 'cancelled', 'Отменена'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='Идентификатор заяки на выплату')
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Сумма выплаты')
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.RUB,
        verbose_name='Валюта'
    )
    recipient_details = models.JSONField(
        verbose_name='Реквизиты получателя',
        help_text='Банковские реквизиты в формате JSON'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='Статус заявки'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание или комментарий',
        help_text='Дополнительная информация о заявке'
    )

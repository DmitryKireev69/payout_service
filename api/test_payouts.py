import json
from decimal import Decimal

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from api.models import PayoutClaim
from unittest.mock import patch
import uuid


class TestsAPI(TestCase):
    """Тесты API для модели PayoutClaim."""

    def setUp(self):
        """Настройка тестовых данных и клиента перед каждым тестом."""
        self.client = APIClient()
        self.data = {
            "amount": "15000.75",
            "currency": "RUB",
            "recipient_details": json.dumps({
                "bank_name": "Тинькофф",
                "account_number": "4070",
                "bik": "044525974",
                "recipient_name": "ИП Иванов Иван Иванович",
                "inn": "771234567890",
                "kpp": "773401001",
                "correspondent_account": "30101810400000000225",
                "recipient_address": "г. Москва, ул. Ленина, д. 1",
                "payment_purpose": "Оплата по договору №123"
            })
        }

        self.payout = PayoutClaim.objects.create(**self.data)

    def test_get_list(self):
        """Проверка получения списка выплат через API (GET /api/payouts/)."""
        url = reverse("payout-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['amount'], '15000.75')

    def test_get_detail(self):
        """Проверка получения детальной информации о выплате (GET /api/payouts/<pk>/)."""
        url = reverse("payout-detail", kwargs={'pk': self.payout.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['currency'], "RUB")

    def test_post_create(self):
        """Проверка создания новой выплаты через API (POST /api/payouts/)."""
        url = reverse("payout-list")
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PayoutClaim.objects.count(), 2)

    def test_put_update(self):
        """Проверка обновления существующей выплаты через API (PUT /api/payouts/<pk>/)."""

        url = reverse("payout-detail", kwargs={'pk': self.payout.pk})
        data = {"amount": "20000.95", "currency": "USD", "recipient_details": self.data.get('recipient_details')}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.payout.refresh_from_db()
        self.assertEqual(self.payout.amount, Decimal("20000.95"))
        self.assertEqual(self.payout.currency, "USD")

    def test_delete_destroy(self):
        """Проверка удаления выплаты через API (DELETE /api/payouts/<pk>/)."""
        url = reverse("payout-detail", kwargs={'pk': self.payout.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PayoutClaim.objects.count(), 0)

    def test_create_calls_celery_task(self):
        """Проверка, что при создании выплаты вызывается Celery-задача."""
        url = reverse("payout-list")
        data = self.data.copy()  # новые данные для POST

        # Мокаем Celery-задачу
        with patch("api.tasks.process_payout.delay") as mock_task:
            response = self.client.post(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            payout_id = response.data["id"]
            mock_task.assert_called_once_with(uuid.UUID(payout_id))

from decimal import Decimal

from rest_framework import serializers
from .models import PayoutClaim

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayoutClaim
        fields = '__all__'

    def validate(self, data):
        """
        Валидация всех полей
        """
        errors = {}

        required_fields = ['amount', 'recipient_details']
        for field in required_fields:
            if field not in data:
                errors[field] = ['Это поле обязательно.']

        amount = data.get('amount')
        if amount > Decimal('99,999,999.99'):
            errors.setdefault('amount', []).append('Сумма слишком большая.')

        if errors:
            raise serializers.ValidationError(errors)

        return data


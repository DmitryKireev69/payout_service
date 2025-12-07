from rest_framework import viewsets
from .models import PayoutClaim
from .serializers import PaymentSerializer
from .tasks import process_payout


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = PayoutClaim.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        payout_claim = serializer.save()
        process_payout.delay(payout_claim.id)

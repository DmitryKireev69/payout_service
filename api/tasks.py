import time
import logging
from celery import shared_task
from .models import PayoutClaim

logger = logging.getLogger(__name__)

@shared_task
def process_payout(payout_id):
    logger.info(f"Начало обработки заявки с ID {payout_id}")

    try:
        app = PayoutClaim.objects.get(id=payout_id)
    except PayoutClaim.DoesNotExist:
        logger.error(f"Заявка с ID {payout_id} не найдена")
        return

    app.status = app.Status.PROCESSING
    app.save()
    logger.info(f"Заявке {payout_id} присвоен статус 'В обработке'")

    # Имитируем длительную обработку
    time.sleep(5)

    logger.info(f"Обработка заявки {payout_id} завершена")

    # Ставим окончательный статус
    app.status = app.Status.PROCESSED
    app.save()
    logger.info(f"Заявке {payout_id} присвоен статус 'обработана'")

    return f"Заявка {payout_id} успешно обработана"

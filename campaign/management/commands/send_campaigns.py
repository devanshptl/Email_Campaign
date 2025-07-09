from django.core.management.base import BaseCommand
from campaign.tasks import send_campaign_batch


class Command(BaseCommand):
    help = "Send daily email campaigns to all active subscribers"

    def handle(self, *args, **kwargs):
        send_campaign_batch.delay()
        self.stdout.write(self.style.SUCCESS("Campaigns sent via Celery"))

from django.core.management.base import BaseCommand
from campaign.tasks import send_daily_campaign


class Command(BaseCommand):
    help = "Send daily email campaigns to all active subscribers"

    def handle(self, *args, **kwargs):
        send_daily_campaign.delay()
        self.stdout.write(self.style.SUCCESS("Campaigns sent via Celery"))

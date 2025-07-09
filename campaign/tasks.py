from celery import shared_task
from concurrent.futures import ThreadPoolExecutor
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from campaign.models import Campaign, Subscriber
from datetime import date


def send_email(email, subject, html, plain):
    send_mail(
        subject=subject,
        message=plain,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        html_message=html,
        fail_silently=False,
    )


@shared_task
def send_campaign_batch():
    campaigns = Campaign.objects.filter(published_date=date.today())
    if not campaigns.exists():
        return

    subscribers = list(
        Subscriber.objects.filter(is_active=True).values_list("email", flat=True)
    )

    for campaign in campaigns:
        subject = campaign.subject
        plain = campaign.plain_text_content

        html = campaign.html_content or render_to_string(
            "email_template.html",
            {
                "subject": subject,
                "preview_text": campaign.preview_text,
                "article_url": campaign.article_url,
                "plain_text_content": plain,
            },
        )
        # Use ThreadPoolExecutor to send emails concurrently
        with ThreadPoolExecutor(max_workers=10) as executor:
            for email in subscribers:
                executor.submit(send_email, email, subject, html, plain)

from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .models import Campaign, Subscriber
from datetime import date
from django.conf import settings


@shared_task
def send_campaign_email_task(email, subject, html, plain):
    send_mail(
        subject=subject,
        message=plain,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        html_message=html,
        fail_silently=False,
    )


@shared_task
def send_daily_campaign():
    today = date.today()
    campaigns = Campaign.objects.filter(published_date=today)
    active_subscribers = list(
        Subscriber.objects.filter(is_active=True).values_list("email", flat=True)
    )

    for campaign in campaigns:
        if campaign.html_content:
            html = campaign.html_content
        else:
            html = render_to_string(
                "email_template.html",
                {
                    "subject": campaign.subject,
                    "preview_text": campaign.preview_text,
                    "article_url": campaign.article_url,
                    "plain_text_content": campaign.plain_text_content,
                },
            )

        for email in active_subscribers:
            send_campaign_email_task.delay(
                email, campaign.subject, html, campaign.plain_text_content
            )

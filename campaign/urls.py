from django.urls import path
from .views import SubscribeView, UnsubscribeView

urlpatterns = [
    path("subscribe/", SubscribeView.as_view()),
    path("unsubscribe/", UnsubscribeView.as_view()),
]

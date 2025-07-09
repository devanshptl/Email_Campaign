from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Subscriber
from .serializers import SubscriberSerializer


class SubscribeView(APIView):
    def post(self, request):
        serializer = SubscriberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Subscribed"}, status=201)
        return Response(serializer.errors, status=400)


class UnsubscribeView(APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            subscriber = Subscriber.objects.get(email=email)
            subscriber.is_active = False
            subscriber.save()
            return Response({"message": "Unsubscribed successfully."})
        except Subscriber.DoesNotExist:
            return Response({"error": "Subscriber not found."}, status=404)

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

VERIFY_TOKEN = "mysecrettoken123"

@csrf_exempt
def whatsapp_webhook(request):

    # Webhook verification
    if request.method == "GET":
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return HttpResponse(challenge, status=200)
        else:
            return HttpResponse("Verification failed", status=403)

    # Incoming message
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            print("Incoming Data:", body)
        except Exception as e:
            print("Error:", e)

        return JsonResponse({"status": "received"}, status=200)

    return JsonResponse({"status": "invalid request"}, status=400)

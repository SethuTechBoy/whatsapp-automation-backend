from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests

VERIFY_TOKEN = "mysecrettoken123"

WHATSAPP_TOKEN = "EAASI3WSjMZA8BQ8AP0AqshFjkvTdOUeLwI25vmyxDs3WbNZCpRvZBqAEKmIsArWE13mipqDsnZBiWBt21QI0VatN7XRiRm7GP23R8sNH986ChOaf5Spnw7d4KX1ah1ImZCem8xrRR1FmgZBaSJLTeZBdJpMaNHDVZBUIVSrEo4wn08abHS6Ie9lUNa9zENREz5jDJIL2eJsNPZBdFWxle2fme0j4ujA4AVvU7sCAlgdIQ"

PHONE_NUMBER_ID = "1065650129956489"


def send_whatsapp_message(to):
    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    # Template message (Sandbox safe)
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": {
            "name": "jaspers_market_plain_text_v1",
            "language": {
                "code": "en_US"
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)
    print("Send Response:", response.text)


@csrf_exempt
def whatsapp_webhook(request):

    if request.method == "HEAD":
        return HttpResponse("ok")

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

            entry = body["entry"][0]
            changes = entry["changes"][0]
            value = changes["value"]

            messages = value.get("messages")

            if messages:
                phone = messages[0]["from"]
                text = messages[0]["text"]["body"]

                print("User:", phone)
                print("Message:", text)

                # Auto reply
                send_whatsapp_message(phone)

        except Exception as e:
            print("Error:", e)

        return JsonResponse({"status": "received"}, status=200)

    return HttpResponse("ok")

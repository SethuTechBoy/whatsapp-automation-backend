from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests

VERIFY_TOKEN = "mysecrettoken123"

# 👉 Meta la irukum Permanent Token
WHATSAPP_TOKEN = "PASTE_YOUR_PERMANENT_TOKEN"

# 👉 Meta la irukum Phone Number ID
PHONE_NUMBER_ID = "PASTE_YOUR_PHONE_NUMBER_ID"


def send_whatsapp_message(to, message):
    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "body": message
        }
    }

    response = requests.post(url, headers=headers, json=data)
    print("Send Response:", response.text)


@csrf_exempt
def whatsapp_webhook(request):

    # Handle HEAD request
    if request.method == "HEAD":
        return HttpResponse("ok")

    # 🔹 Webhook verification
    if request.method == "GET":
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return HttpResponse(challenge, status=200)
        else:
            return HttpResponse("Verification failed", status=403)

    # 🔥 Incoming message
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

                # 🔥 AUTO REPLY
                send_whatsapp_message(
                    phone,
                    "Hello 👋\n\nThanks for contacting us.\nHow can we help you?"
                )

        except Exception as e:
            print("Error:", e)

        return JsonResponse({"status": "received"}, status=200)

    return HttpResponse("ok")

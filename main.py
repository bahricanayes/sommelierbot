
from flask import Flask, request
import requests

app = Flask(__name__)

# WhatsApp API bilgileri
VERIFY_TOKEN = 'bahrican_token'
ACCESS_TOKEN = 'EAARJEJjvXRMBOZBkpiPxZB4Iqi7SVMpVusFNnlEZBIuzR8ygc8e2LV8GiGmXb3O6uKdAQs3TxyON1biSE26vEifbSnrKAQe8O57oOq3ladrSVPJQKi36JHUppbtJgbJlrc8T43BPX0OFAY1HQbQ3vx2tlLdrxMrh1UzKgKKVLbLjV2qEJQFzQ5KZAbJ7LmZAeh7wYyK4Bp6ENgSgGsgRZAWvDCzcEZD'
PHONE_NUMBER_ID = '614144941788819'

def send_whatsapp_message(phone_number, message_text):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {"body": message_text}
    }
    response = requests.post(url, headers=headers, json=payload)
    print(f"Mesaj gönderildi. Status Code: {response.status_code}, Response: {response.text}")

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return 'Verification token mismatch', 403

    if request.method == 'POST':
        data = request.get_json()
        print(f"Gelen veri: {data}")

        try:
            phone_number = data['entry'][0]['changes'][0]['value']['messages'][0]['from']
            message_text = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']

            print(f"Gelen mesaj: {message_text} - Gönderen: {phone_number}")

            cevap_mesaji = f"Mesajınızı aldım: {message_text}"
            send_whatsapp_message(phone_number, cevap_mesaji)

        except Exception as e:
            print(f"POST işleme hatası: {e}")

        return 'EVENT_RECEIVED', 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)



from flask import Flask, request
import requests

app = Flask(__name__)

VERIFY_TOKEN = 'bahrican_token'
ACCESS_TOKEN = 'EAARJEJjvXRMBOxqE02GBCykqy6Rh7YMISs4fDQWhZBHAkLg4B4mQDNaEH9X1AKb9UlL4kdXZAyZCUSoMLSwURI0yedgR2QjVbixCbl0iNrtxGrN0B3OfIfowdiIQMeGEF8Co9rjUIJWpywFyiAZBasQUAE6anJ4lYVQrziIpAAMJvepu4VtEr9biMPUwT0HWVsA1x5WQQZCk8oI1CVHTGbZAn6NTcZD'
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
    print(f"[SEND] Status Code: {response.status_code}")
    print(f"[SEND] Response: {response.text}")

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if token == VERIFY_TOKEN:
            return challenge, 200
        return 'Token mismatch', 403

    if request.method == 'POST':
        data = request.get_json()
        print("[POST] Webhook çağrıldı!")
        print("[POST] Gelen veri:")
        print(data)

        try:
            phone_number = data['entry'][0]['changes'][0]['value']['messages'][0]['from']
            message_text = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
            print(f"[POST] Gönderen: {phone_number}, Mesaj: {message_text}")
            cevap = f"Mesajınızı aldım: {message_text}"
            send_whatsapp_message(phone_number, cevap)
        except Exception as e:
            print(f"[ERROR] POST işleme hatası: {e}")

        return 'EVENT_RECEIVED', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

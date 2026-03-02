import os
from twilio.rest import Client

def send_sms(to_number: str, body: str) -> str:
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    from_number = os.environ.get("TWILIO_FROM_NUMBER")

    if not (account_sid and auth_token and from_number):
        raise RuntimeError("Twilio env vars missing (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER)")

    client = Client(account_sid, auth_token)
    msg = client.messages.create(body=body, from_=from_number, to=to_number)
    return msg.sid
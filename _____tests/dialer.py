from twilio.rest import Client

account_sid = ''
auth_token = ''
client = Client()

message = client.messages.create(
         body='This is the ship that made the Kessel Run in fourteen parsecs?',
         from_='+15005550006',
         to='+212645538791'
     )

print(message.sid)

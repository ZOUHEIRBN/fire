from twilio.rest import Client

account_sid = 'ACe35eb0fa4b0da6a82455300ffe880bdb'
auth_token = '5d78043bfb4d81c66c1fb89d5c518b9f'
client = Client()

message = client.messages.create(
         body='This is the ship that made the Kessel Run in fourteen parsecs?',
         from_='+15005550006',
         to='+212645538791'
     )

print(message.sid)
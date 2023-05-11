from twilio.rest import Client
from dotenv import dotenv_values
from messages import init_firestore, MessageHandler
from bot import Bot

def make_client() -> Client:
    config = dotenv_values(".env") 
    account_sid = config['TWILIO_ACCOUNT_SID']
    auth_token = config['TWILIO_AUTH_TOKEN']
    return Client(account_sid, auth_token)

def send(client:Client, message_response:str, to: str)->str:
    message = client.messages \
    .create(
         body=message_response,
         from_='+15748574623',
         to=f'{to}'
     )
    return message.sid

def sms(request):

    number = request.form['From']
    message_body = request.form['Body']
    print(f'received {message_body} from {number}')
    db = init_firestore(False)
    message_handler = MessageHandler(db)
    print('initialized firestore')
    message_handler.write_message(number, 'user', message_body)
    print('wrote message to firestore')
    bot = Bot(number, message_handler)
    bot_response = bot.respond()
    print(f'got bot response {bot_response}')
    message_handler.write_message(number, 'assistant', bot_response)
    print('wrote bot_response to firebase')
    twilio_client = make_client()
    result = send(twilio_client, bot_response, number)
    print('sent bot response to twilio')
    return str(result)
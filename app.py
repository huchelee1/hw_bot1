#Python libraries that we need to import for our bot
from flask import Flask, request
from pymessenger.bot import Bot
import os 
import threading
app = Flask(__name__)
ACCESS_TOKEN = 'EAAFwNZBxNu4kBADCKS6NqESrQ626KIl0gAAmklTqBg9T56cnZBFg8jbKofZAkU7RJs96j5PrX2ZCqAPlZAIZBpCZBjD8Shp3qPzMLrSe1zCqZAjlZCfDlSx6wndHynvvY33CdtDXVPDUtRGqsumjKnOdENsA15VcCAQvlzWetaIYI10AahkhveyPx'   #ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = 'VERIFY_TOKEN'   #VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot (ACCESS_TOKEN)
init_message=False

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    global init_message
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
            messaging=event['messaging']
            for message in messaging:
                if message.get('message'):
                    recipient_id = message['sender']['id']
                    #text_message = message['message'].get('text')
                #Facebook Messenger ID for user so we know where to send response back to
                    if message['message'].get('text')and init_message==False:
                        response_sent_text = initial_message()
                        send_message(recipient_id, response_sent_text)
                        init_message=True
                        if len(message['message'].get('text')>3 and init_message==True:
                            response_sent_text = follow_up()
                            send_message(recipient_id, response_sent_text)
                    
                #if user sends us a GIF, photo,video, or any other non-text item
                    if message['message'].get('attachments'):
                        response_sent_nontext = get_message()
                        send_message(recipient_id, response_sent_nontext)
            
    return "Message Processed"

def time_message():
    response= random.choice[("hey! How's your homework going?"),("Hope your homework is going well!"),("Don't forget about good homework habits! :)")]
    return(response)
    
                            

def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def follow_up():
    sample_responses = "Okay, thanks"
    # return selected item to the user
    return (sample_responses)


#chooses a random message to send to the user
def initial_message():
    global init_message
    sample_responses = "Hello, this is the homework bot 2.0! This is a program that will help remind you to do your homework! We just need some information from you first. You're name is needed, teacher/guardian e-mail, and classes are needed"
    # return selected item to the user
    return (sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()

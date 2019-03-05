#Python libraries that we need to import for our bot
from flask import Flask, request
from pymessenger.bot import Bot
import os 
import threading
import random

app = Flask(__name__) #sets the Flask output to app.
ACCESS_TOKEN = 'EAAFwNZBxNu4kBADCKS6NqESrQ626KIl0gAAmklTqBg9T56cnZBFg8jbKofZAkU7RJs96j5PrX2ZCqAPlZAIZBpCZBjD8Shp3qPzMLrSe1zCqZAjlZCfDlSx6wndHynvvY33CdtDXVPDUtRGqsumjKnOdENsA15VcCAQvlzWetaIYI10AahkhveyPx'   #ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = 'VERIFY_TOKEN'   #VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot (ACCESS_TOKEN)

# simple booleans that assist with the determining that some elements of the program has been fullfiled.
init_message=False 
timerbool=False

# This part of the program uses Flask. The methods GET and POST allows the data from facebook messenger to be obtained as well as the
# messages that are sent from the program. "GET" is used in this program to recieve the verification token that Facebook needs to be able
# to allow this program to configure to the messenger bot. "POST" is the opposite in that it sends the user information such as text.
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    global init_message, timerbool
    if request.method == 'GET': 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    # this part of the program consist of the "POST" and due to the first part of the function to be an if statement with a  "GET" method
    else:
        # recieves an input from a bot
       output = request.get_json() #Some json elements are added within the code to order the outputs of the users identitification 
       for event in output['entry']:# and messages.
            messaging=event['messaging']
            for message in messaging:
                if message.get('message'):
                    recipient_id = message['sender']['id'] # This section is used for recognizing who to send a message to.
                    if message['message'].get('text')and init_message==False:
                        response_sent_text = initial_message()
                        send_message(recipient_id, response_sent_text)
                        init_message=True
                    if len(message['message'].get('text'))>3 and init_message==True:
                        response_sent_text = follow_up()
                        send_message(recipient_id, response_sent_text)
                        #set_time()
                    #if timerbool==True:
                        #response_sent_text= time_message()
                        #send_message(recipient_id, response_sent_text)
    return "Message Processed"

# this is the timer that will be used to send messages periodcally           
def set_time():
    t= timer(30.0,global_time)
    t.start()
    return("time up")

# This function is used for setting timerbool to be true and cause the if statement in recieve_message to send messages periodically
def global_time():
    global timerbool
    return timerbool=True

# this function is used as the reminders throughout the day. 
def time_message():
    response=["hey! How's your homework going?","Hope your homework is going well!","Don't forget about good homework habits! :)"]
    return random.choice(response)
    
                            
# this function takes the token procided by facebook and makes sure that it maches with the token sent by the code (VEFIFY_TOKEN).
def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

# follow up is a part of the code that will send a message after the initial message is sent. This function is simply a confirmation 
# for the user. 
def follow_up():
    sample_responses = "Okay, thanks"
    # return selected item to the user
    return (sample_responses)


#This function introduces the user to the Homework bot and is just the message to inform the user. 
def initial_message():
    global init_message
    sample_responses = "Hello, this is the homework bot 2.0! This is a program that will help remind you to do your homework! Please let us know the times of when to remind you(example text: 4:00 PM). Note:This is the time may not be exact to the time of yours due to the server placement(mid west timezone US)"
    # return selected item to the user
    return (sample_responses)

#uses PyMessenger to send response to user. PyMessenger is a code that exist within GitHub that has functions to help with the 
#complications in the process of sending messages to a user. 
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

#Last line of code that allows the program to run in a loop. 
if __name__ == "__main__":
    app.run()

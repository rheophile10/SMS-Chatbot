this sits on a google cloud function. 

It 
- receives POSTs from TWILIO, 
- logs them to firebase, 
- retrieves conversation history and context for that number from firebase, 
- gets OpenAI to complete the chat with a response, 
- logs the response to firebase
- sends the response back to the source phone number

So you can do this


![image](https://github.com/rheophile10/SMS-Chatbot/assets/60486447/5a5167c0-0174-404e-92ca-10b459e102c8)

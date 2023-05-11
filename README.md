this sits on a google cloud function. 

It 
    -receives POSTs from TWILIO, 
    -logs them to firebase, 
    -retrieves conversation history and context for that number from firebase, 
    -gets OpenAI to complete the chat with a response, 
    -logs the response to firebase
    -sends the response back to the source phone number


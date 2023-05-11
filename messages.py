import firebase_admin
from firebase_admin import firestore, credentials
from pathlib import Path
from datetime import datetime
from functools import reduce
from typing import List, Dict, Any

def init_firestore(local_json_init:bool=True)->Any:
    if firebase_admin._DEFAULT_APP_NAME not in firebase_admin._apps:
        if local_json_init:
            service_path = Path(__file__) / 'serviceAccount.json'
            cred = credentials.Certificate(service_path)
            app = firebase_admin.initialize_app(cred)
        else:
            app = firebase_admin.initialize_app()
    return firestore.client()

class MessageHandler:
    def __init__(self, firestore_client:Any)->None:
        self.db = firestore_client
        
    def write_message(self, conversation: str, role: str, body: str) -> None:
        message = {
            'conversation': conversation,
            'role': role,
            'content': body,
            'timestamp': datetime.now(),
        }
        self.db.collection(u'Conversations').add(message)

    def fetch_messages(self, conversation: str, limit:int = 50) -> List[Dict[str, Any]]:
        query = self.db.collection(u'Conversations') \
            .where('conversation', '==', conversation) \
            .order_by('timestamp', direction=firestore.Query.ASCENDING) \
            .limit(limit)
        docs = []
        for doc in query.stream():
            doc = doc.to_dict()
            docs.append({'role': doc['role'], 'content':doc['content']})
        return docs

    def write_context(self, conversation:str, context:str) -> None:
        context = {
            'conversation':conversation,
            'context':context
        }
        self.db.collection(u'Contexts').add(context)

    def fetch_context(self, conversation:str, limit:int = 50) -> List[Dict[str, str]]:
        query = self.db.collection(u'Contexts') \
            .where('conversation', '==', conversation) \
            .order_by('timestamp', direction=firestore.Query.ASCENDING) \
            .limit(limit)
        contexts = [doc.to_dict()['context'] for doc in query.stream()]
        context = '\n'.join(contexts) 
        return [{'role':'system', 'content':context}]
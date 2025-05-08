import firebase_admin
from firebase_admin import credentials, firestore
from pydantic import BaseModel
from icecream import ic
import os

# Assuming Article is defined somewhere like this:
class Article(BaseModel):
    """Model representing an article from Firestore"""
    title: str
    link: str
    content: str

# Initialize Firebase Admin
'''
def init_firebase(project_id, credential_path):
    try:
        # Initialize Firebase
        cred = credentials.Certificate(credential_path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        return db
    except Exception as e:
        print(f"An error occurred: {e}")
'''
# Function to insert article into Firestore
def insert_article(db, article: Article):
    try:
        # Ensure the collection and document IDs are correct
        collection_ref = db.collection("articles")
        article_data = article.dict()  # Convert Article object to dict
        collection_ref.add(article_data)
        print("Article inserted successfully.")
    except Exception as e:
        print(f"An error occurred while inserting article: {e}")

# Usage
if __name__ == "__main__":
        try:
        # Construct the path to the credentials file. Use a relative path.

            cred_path = os.path.join(os.path.dirname(__file__), "firebase_auth.json")
            ic(cred_path)
            if not os.path.exists(cred_path):
                raise FileNotFoundError(f"Firebase credentials file not found at: {cred_path}")

            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            
            ic("Firebase initialized successfully.")
        except Exception as e:
            ic(f"Error initializing Firebase: {e}")
            db = None  # Set to None in case of failure
    
        if db:
            article = Article(title="Example Title_2", link="https://example.com/blabla", content="This is an example article_2.")
            insert_article(db, article)
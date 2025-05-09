import firebase_admin
from firebase_admin import credentials, firestore
from pydantic import BaseModel
from icecream import ic
import os

# Assuming Article is defined somewhere like this:
class Article(BaseModel):
    title: str
    content: str
    link: str
    uid: str | None = None  # Add uid field, initialized as None



# Function to insert article into Firestore
def insert_article(db: firestore.client, article: Article):
    try:
        # Ensure the collection and document IDs are correct
        collection_ref = db.collection("articles")
        article_data = article.model_dump()  # Convert Article object to dict
        _, doc_ref = collection_ref.add(article_data)
        uid = doc_ref.id
        # Update the document in Firestore with the generated UID
        doc_ref.update({"uid": uid})
        print(f"Article inserted successfully with UID: {uid}")
        return uid
    except Exception as e:
        print(f"An error occurred while inserting article: {e}")
        return None

# Usage
if __name__ == "__main__":
        try:


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
            article = Article(title="Example Title_", link="https://vivaverdelife.com/terms", content="This is an example article_5.")
            generated_uid = insert_article(db, article)
            if generated_uid:
                ic(f"Article inserted with UID: {generated_uid}")
            else:
                ic("Failed to insert article.")
            
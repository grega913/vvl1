import firebase_admin
from firebase_admin import credentials, firestore
from pydantic import BaseModel
from icecream import ic
import os


from src_agentz.models.article import Article


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


def upload_image_to_firebase_storage(image_path: str, uid: str, content_type: str = "image/jpeg"):
    """Uploads an image to Firebase Storage with the given UID as filename.
    
    Args:
        image_path: Path to the local image file
        uid: Unique identifier to use as filename (without extension)
        content_type: MIME type of the image (default: image/jpeg)
    """
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found at: {image_path}")
            
        bucket = firebase_admin.storage.bucket()
        # Get file extension from original filename
        file_ext = os.path.splitext(image_path)[1].lower()
        blob = bucket.blob(f"images/{uid}{file_ext}")
        
        # Set content type for proper browser rendering
        blob.content_type = content_type
        blob.upload_from_filename(image_path)
        
        # Make the blob publicly viewable
        blob.make_public()
        
        print(f"Image uploaded successfully to: {blob.public_url}")
        return blob.public_url
    except Exception as e:
        print(f"Error uploading image: {e}")
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
                
                # Test uploading images
                tmp_dir = os.path.join(os.path.dirname(__file__), "source_agno_tmp")
                image1 = os.path.join(tmp_dir, "test1.jpg")
                image2 = os.path.join(tmp_dir, "test2.png")
                
                if os.path.exists(image1):
                    upload_image_to_firebase_storage(image1, f"{generated_uid}_1")
                if os.path.exists(image2):
                    upload_image_to_firebase_storage(image2, f"{generated_uid}_2", "image/png")
            else:
                ic("Failed to insert article.")
            

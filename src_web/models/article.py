from pydantic import BaseModel

class Article(BaseModel):
    """Model representing an article from Firestore"""
    title: str
    link: str
    content: str

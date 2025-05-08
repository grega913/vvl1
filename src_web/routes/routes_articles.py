from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from icecream import ic
from typing import List, Dict
import sys

from models.article import Article

blogs_router = APIRouter()
templates = Jinja2Templates(directory="src_web/static/templates/articles/")

@blogs_router.get("/basic_article", response_class=HTMLResponse)
async def basic_article(request: Request):
    return templates.TemplateResponse(request=request, name="basic_article.html")



@blogs_router.get("/article/{article_id}")
async def article(article_id: str, request: Request):
    """Retrieve a blog article from Firestore by its ID."""
    db = request.app.state.firestore_db
    if db is None:
        raise HTTPException(status_code=500, detail="Firebase not initialized.")
    try:

        doc_ref = db.collection("articles").document(article_id)
        doc_snapshot = doc_ref.get()  # This is synchronous in Firestore admin SDK
        if doc_snapshot.exists:
            article_data = doc_snapshot.to_dict()



            article = Article(**article_data)
            return templates.TemplateResponse(
                request=request,
                name="article_from_fb.html",
                context={"article": article}
            )
        else:
            raise HTTPException(status_code=404, detail=f"Article with id {article_id} not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching article: {e}")
    


@blogs_router.get("/all_articles/")
async def all_articles(request: Request) -> List[Dict]:
    """Retrieve all articles from the Firestore 'articles' collection."""
    db = request.app.state.firestore_db
    if db is None:
        raise HTTPException(status_code=500, detail="Firebase not initialized.")
    try:
        articles_collection = db.collection("articles")
        docs = articles_collection.get()  # Get all documents in the collection

        articles = []
        for doc in docs:
            if doc.exists: # Check if the document exists.
                articles.append(doc.to_dict()) # Convert document snapshot to dictionary and add to the list
            else:
                print(f"Document {doc.id} does not exist") # Log the non-existent doc.

        return articles
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching articles: {e}")



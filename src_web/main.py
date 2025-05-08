# region Imports

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from icecream import ic
import firebase_admin
from firebase_admin import credentials, firestore
import uvicorn
import os
import sys
import time 

# endregion

# region Lifespan - things happening before first request 
# https://fastapi.tiangolo.com/advanced/events/#lifespan

src_web_path = os.path.dirname(os.path.abspath(__file__))


# Add src_web to the beginning of sys.path
sys.path.insert(0, src_web_path)




from routes.routes_basic import basic_router
from routes.routes_articles import blogs_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.  Initializes Firebase on startup.
    """
    ic(lifespan)


    
    try:
        # Construct the path to the credentials file. Use a relative path.

        cred_path = os.path.join(os.path.dirname(__file__), "firebase_auth.json")
        ic(cred_path)
        if not os.path.exists(cred_path):
            raise FileNotFoundError(f"Firebase credentials file not found at: {cred_path}")

        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        app.state.firestore_db = db
        ic("Firebase initialized successfully.")
    except Exception as e:
        ic(f"Error initializing Firebase: {e}")
        app.state.firestore_db = None  # Set to None in case of failure

    yield  # This is where the application runs

    # Clean up resources on shutdown (if needed)
    if "firestore_db" in app.state:
        #  No need to explicitly close the client in most cases, but you could
        #  add cleanup here if you had other resources to manage.
        print("Firebase resources cleaned up (if needed).")
        pass # Remove pass and add any cleanup.
    





app = FastAPI(lifespan=lifespan)

app.include_router(blogs_router)
app.include_router(basic_router)


# mapping static file
# app.mount("/static", StaticFiles(directory="src_web/static", follow_symlink=True), name="static") 
static_dir = os.path.join(os.path.dirname(__file__), 'static')
app.mount("/static", StaticFiles(directory=static_dir, follow_symlink=True), name="static")


if __name__ == "__main__":
    ic(sys.path)
    uvicorn.run("main:app", reload=True)
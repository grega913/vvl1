from agno.agent import Agent
from agno.models.deepseek import DeepSeek # type: ignore
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools import tool
import random
from icecream import ic
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, firestore
import os
import sys

from textwrap import dedent
sys.path.insert(0, os.path.abspath('./'))
from src_agentz.models.article import Article


@tool(show_result=True, stop_after_tool_call=True)
def insert_article_into_Firestore(article: Article)->str:
    """Inserts the article into Firestore and returns the generated UID. Ignore validation errors at this point."""
    ic(" def insert_article_into_Firestore")

    try:
        cred_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "firebase_auth.json")

        if not os.path.exists(cred_path):
            raise FileNotFoundError(f"Firebase credentials file not found at: {cred_path}")
        
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()

        collection_ref = db.collection("articles")
        article_data = article.model_dump()  # Convert Article object to dict
        # Add server timestamp
        article_data["created_at"] = firestore.SERVER_TIMESTAMP
        _, doc_ref = collection_ref.add(article_data)
        uid = doc_ref.id
        # Update the document in Firestore with the generated UID
        doc_ref.update({
            "uid": uid,
            "created_at": firestore.SERVER_TIMESTAMP  # Ensure timestamp is set
        })
        print(f"Article inserted successfully with UID: {uid}")
        return uid


    except Exception as e:
            ic(f"Error initializing Firebase: {e}")
            db = None  # Set to None in case of failure
            return "Error inserting article"

agent_firestore = Agent(
    name="agent_firestore",
    model=DeepSeek(),
    tools=[insert_article_into_Firestore],
    markdown=True,
    show_tool_calls=True,
    debug_mode=True,
    description=dedent("""\
        "You are an agent responsible for communicating with Firestore.
         Make sure to use appropriate tool.
         When inserting article, only use appropriate fields from the class Article,
         which are: title, content, affiliateLinks, uid, created_at.\
    """)
)


if __name__ == "__main__":
    agent_firestore.print_response("Insert article into Firestore. If there are no known values for particular field in Article instance, just make up something simple.  If there's no value for links, just use default one from where the class is defined.", stream=True)

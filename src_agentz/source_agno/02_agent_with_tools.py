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


# Assuming Article is defined somewhere like this:
class Article(BaseModel):
    title: str | None = "my title"  # Add title field, initialized as None
    content: str | None = "my content"  # Add content field, initialized as None
    link: str = "https://vivaverdelife.com/terms"  # Add link field, initialized as None
    uid: str | None = None  # Add uid field, initialized as None
    created_at: str | None = None  # Will be set to server timestamp


@tool(show_result=True, stop_after_tool_call=True)
def get_weather(city: str) -> str:
    """Get the weather for a city."""
    # In a real implementation, this would call a weather API
    weather_conditions = ["sunny", "cloudy", "rainy", "snowy", "windy"]
    random_weather = random.choice(weather_conditions)

    return f"The weather in {city} is {random_weather}."




@tool(show_result=True, stop_after_tool_call=True)
def insert_article_into_Firestore(article: Article)->str:
    """Inserts the article into Firestore and returns the generated UID."""
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
    model=DeepSeek(),
    tools=[insert_article_into_Firestore],
    markdown=True,
    show_tool_calls=True,
    debug_mode=True,
    description="You are an agent responsible for communicating with Firestore. Make sure to use appropriate tool. When inserting article, only use appropriate fields from the class Article, which are: title, content, link, uid, created_at."
,
)


if __name__ == "__main__":
    agent_firestore.print_response("Insert article into Firestore. If there are no known values for particular field in Article instance, just make up something simple. The content should be 3 sentences long. If there's no value for link, just use default one from where the class is defined.", stream=True)

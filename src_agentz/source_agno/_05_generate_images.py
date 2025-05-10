from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.dalle import DalleTools
from agno.utils.media import download_image
from pathlib import Path
from icecream import ic
from agno.tools import tool
import datetime
import firebase_admin
from firebase_admin import storage
import os
import sys



@tool(show_result=True, stop_after_tool_call=True)
def save_images_to_disc()-> str:
    """Gets images from agent and saves them to disc"""

    ic("def save_images_to_disc")
    try:
        images = agent_dalle.get_images()
        if images and isinstance(images, list):
            for image_response in images:
            # Get current time
                current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{current_time}.jpg"

                download_image(
                    url=image_response.url,
                    output_path=Path(__file__).parent.joinpath(f"tmp/{filename}"),
                )


                


            return f"Images saved successfully to the disc"

    except Exception as e:
        ic(f"Error saving images: {e}")
        return "Error saving images"


@tool(show_result=True, stop_after_tool_call=True)
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
            
        bucket = storage.bucket()
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







agent_dalle = Agent(
    name="agent_dalle",
    model=OpenAIChat(id="gpt-4o"),
    tools=[DalleTools(), save_images_to_disc, upload_image_to_firebase_storage],
    description="You are an AI agent that can generate images using DALL-E.",
    instructions="When the user asks you to create an image, use 'create_image' to create the image. Then save the image to the disc using the `save_image_to_the_disc` tool. After the image is saved to the disc, use upload_image_to_firebase_storage to upload the image to Firebase Storage.",
    markdown=True,
    show_tool_calls=True,
)

#image_agent.print_response("Generate an image of a white siamese cat")
agent_dalle.print_response("A serene outdoor yoga session under a sunny sky, featuring a man over 55 practicing yoga on a mat in a peaceful natural setting, surrounded by trees and flowers. The scene should convey tranquility and mindfulness, with soft sunlight filtering through the leaves, creating a warm and inviting atmosphere.")



'''
images = agent_dalle_tools.get_images()

if images and isinstance(images, list):
    for image_response in images:
        image_url = image_response.url
        print(image_url)
        download_image(
            url=image_url,
            output_path=Path(__file__).parent.joinpath("tmp/nature.jpg"),
       
        )
'''
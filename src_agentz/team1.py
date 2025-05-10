from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.team.team import Team
from textwrap import dedent
from agno.tools.dalle import DalleTools
from icecream import ic


from source_agno._04_agent_articles_with_strucured_output import agent_structured_output_articles
from source_agno._02_agent_firestore import agent_firestore, insert_article_into_Firestore
from source_agno._05_generate_images import agent_dalle, save_images_to_disc



vvl_agent = Team(
    name = "vvl_main_agent",
    model = DeepSeek(),
    mode = "collaborate",
    description = "Viva Verde Life Agent. This agent is responsible for creating articles and inserting them into Firebase. It can also generate images using DALL-E.",
    members=[
        agent_structured_output_articles,
        agent_firestore,
        agent_dalle,
    ],
    share_member_interactions=True,
    show_members_responses=True,
    show_tool_calls=True,
    markdown=True,
    debug_mode=True,
    #tools = [insert_article_into_Firestore, save_images_to_disc],
    add_member_tools_to_system_message=True,
    instructions= dedent("""\
        Delegate tasks to appropriate agents.
        First create an article using the agent_structured_output_articles.
        Then create an image using the agent_dalle.
        Finally, insert the article into Firebase using the agent_firestore.\
        """)


if __name__ == "__main__":

    main_prompt = dedent("""\

        1.  Write an article about the benefits of yoga for mental health of women over 40. For affiliatedLinks just make some dummy links, with example.com and ebay.com as domain.
        3.  Also create an image for the article using appropriate prompt that should depict what is written in the article. Make sure to use the DALL-E tool to create the image. 
        4.  When creating a image prompt make sure to set image size to 1792x1024 and quality to hd. The scenario of image should be natural, weather nice and sunny. Add a person related to the article.
        5.  After the article is created, insert it into Firebase.
        \
    """)


    # Example run with a prompt
    response = vvl_agent.run(main_prompt)
    print(response)




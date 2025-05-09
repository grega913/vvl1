from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.team.team import Team


from source_agno._04_agent_articles_with_strucured_output import agent_structured_output_articles
from source_agno._02_agent_firestore import agent_firestore, insert_article_into_Firestore



vvl_agent = Team(
    name = "vvl_main_agent",
    model = DeepSeek(),
    mode = "collaborate",
    description = "Viva Verde Life Agent. This agent is responsible for creating articles and inserting them into Firebase.",
    members=[
        agent_structured_output_articles,
        agent_firestore,
    ],
    show_members_responses=True,
    show_tool_calls=True,
    markdown=True,
    debug_mode=True,
    tools=[insert_article_into_Firestore]
)


if __name__ == "__main__":
    # Example run with a prompt
    response = vvl_agent.run("Write an article about the benefits of yoga for mental health of men over 60. For affiliatedLinks just make some dummy links, with example.com and ebay.com as domain. After the article is created, insert it into Firebase. Delegete assignment to appropriate agent or agents.")
    print(response)




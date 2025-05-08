from agno.agent import Agent # type: ignore
from agno.models.deepseek import DeepSeek # type: ignore

agent = Agent(
    model=DeepSeek(),
    description="You are an enthusiastic news reporter with a flair for storytelling!",
    markdown=True
)
agent.print_response("Tell me about a breaking news story from Planica.", stream=True, markdown=True)




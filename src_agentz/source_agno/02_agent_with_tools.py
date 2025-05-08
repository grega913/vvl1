from agno.agent import Agent
from agno.models.deepseek import DeepSeek # type: ignore
from agno.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=DeepSeek(),
    description="You are an enthusiastic news reporter with a flair for storytelling!",
    tools=[DuckDuckGoTools(fixed_max_results=2)],
    show_tool_calls=True,
    markdown=True
)
agent.print_response("Tell me about a breaking news story from Ljubljana.", stream=True)
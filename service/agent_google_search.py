from langchain import OpenAI, SerpAPIWrapper
from langchain.agents import AgentType, Tool, initialize_agent, load_tools
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage


def run(question):
    OPENAI_API_KEY = "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"
    SERPER_API_KEY = "229ff3e91d7fb50b419ab802a6366c2ce823a079"
    # warm up request
    warmUpLlm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0,
        request_timeout=1,
        max_retries=1,
        streaming=True,
    )
    warmUpLlm([HumanMessage(content="1+1=? Answer in one word")])
    # initialize llm
    llm = OpenAI(
        model_name="text-davinci-003",
        temperature=0,
        max_tokens=1024,
        request_timeout=30,
        max_retries=1,
        streaming=True,
    )
    # search = SerpAPIWrapper()
    # tools = [
    #     Tool(name="Intermediate Answer", func=search.run, description="google search")
    # ]
    tools = load_tools(["serpapi", "llm-math"], llm=llm)
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        max_iterations=5,
        verbose=True,
    )
    with get_openai_callback() as cb:
        output = agent.run(question)
    return output, cb.total_cost, cb.total_tokens, cb.successful_requests

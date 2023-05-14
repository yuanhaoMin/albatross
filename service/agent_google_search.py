from langchain import OpenAI, SerpAPIWrapper
from langchain.agents import AgentType, Tool, initialize_agent, load_tools
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage


def run(question):
    openai_api_key = "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"
    serper_api_key = "da244df9ed10bbc6eeb85d2708a90435840da9c7904b3cf9a3883c44483a5090"
    # warm up request
    warmUpLlm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=openai_api_key,
        request_timeout=2,
        max_retries=0,
        streaming=True,
    )
    warmUpLlm([HumanMessage(content="1+1=?Answer in one word")])
    # initialize llm
    llm = OpenAI(
        model_name="text-davinci-003",
        temperature=0,
        max_tokens=1024,
        openai_api_key=openai_api_key,
        request_timeout=30,
        max_retries=1,
        streaming=False,
    )
    search = SerpAPIWrapper(
        serpapi_api_key=serper_api_key,
        params={
            "engine": "google",
            "google_domain": "google.com",
            "gl": "cn",
            "hl": "zh-cn",
        },
    )
    tools = [
        Tool(
            name="Google Search",
            func=search.run,
            description="Search Google for recent results",
        )
    ]
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        max_iterations=5,
        return_intermediate_steps=True,
        verbose=False,
    )
    with get_openai_callback() as cb:
        # Input must be a list
        output_data = agent.apply([question])
    final_answer = output_data[0]["output"]
    intermediate_steps = output_data[0]["intermediate_steps"]
    return (
        final_answer,
        intermediate_steps,
        cb.total_cost,
        cb.total_tokens,
        cb.successful_requests,
    )

from langchain import (
    SerpAPIWrapper,
)
from langchain.agents import AgentType, initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage,
)

llm = ChatOpenAI(
    model_name="gpt-3.5-turbo-0613",
    temperature=0,
    openai_api_key="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",
    request_timeout=2,
    max_retries=1,
    streaming=True,
)
search_wrapper = SerpAPIWrapper(
    serpapi_api_key="da244df9ed10bbc6eeb85d2708a90435840da9c7904b3cf9a3883c44483a5090",
    params={
        "engine": "google",
        "google_domain": "google.com",
        "gl": "cn",
        "hl": "zh-cn",
    },
    # params={
    #     "engine": "bing",
    #     "cc": "HK",
    # },
)

tools = [
    Tool(
        name="Search",
        func=search_wrapper.run,
        description="useful for when you dont know the answer. You should ask targeted questions",
    ),
    Tool(
        name="Chinese",
        func=search_wrapper.run,
        description="useful for when you need to answer questions written in chinese. You should ask targeted questions",
    ),
]
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    max_iterations=3,
    return_intermediate_steps=True,
    verbose=False,
)
output_data = agent.apply(["乾坤物联刘文涛"])
final_answer = output_data[0]["output"]
intermediate_steps = output_data[0]["intermediate_steps"]
print("intermediate steps: " + str(intermediate_steps))
print("final answer: " + final_answer)

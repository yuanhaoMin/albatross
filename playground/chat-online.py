from langchain.utilities import GoogleSerperAPIWrapper
from langchain.agents import AgentType, initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage,
)

llm = ChatOpenAI(
    model_name="gpt-3.5-turbo-16k",
    temperature=0,
    openai_api_key="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",
    request_timeout=2,
    max_retries=1,
    streaming=True,
)
search_wrapper = GoogleSerperAPIWrapper(
    serper_api_key="229ff3e91d7fb50b419ab802a6366c2ce823a079",
    k=15,
    gl="cn",
    hl="zh-cn",
)
tools = [
    Tool(
        name="Chinese",
        func=search_wrapper.run,
        description="useful for when you need to answer questions written in chinese. You should ask targeted questions",
    ),
    Tool(
        name="Search",
        func=search_wrapper.run,
        description="useful for when you dont know the answer. You should ask targeted questions",
    ),
    Tool(
        name="DateTime",
        func=search_wrapper.run,
        description="useful for when you need to answer questions related to date time. You should ask targeted questions",
    ),
]
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    max_iterations=3,
    return_intermediate_steps=True,
    verbose=True,
)
output_data = agent.apply(["10家广东省UWB企业"])
final_answer = output_data[0]["output"]
intermediate_steps = output_data[0]["intermediate_steps"]
print("intermediate steps: " + str(intermediate_steps))
print("final answer: " + final_answer)

from langchain import OpenAI, SerpAPIWrapper
from langchain.agents import AgentType, Tool, initialize_agent
from langchain.chat_models import ChatOpenAI
from service.setting_service import get_api_key_settings


def online_search(question):
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo-0613",
        temperature=0,
        openai_api_key=get_api_key_settings().openai_api_key,
        request_timeout=2,
        max_retries=1,
        streaming=True,
    )
    search_wrapper = SerpAPIWrapper(
        serpapi_api_key=get_api_key_settings().serper_api_key,
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
        verbose=False,
    )
    output_data = agent.apply([question])
    final_answer = output_data[0]["output"]
    intermediate_steps = output_data[0]["intermediate_steps"]
    return (final_answer, intermediate_steps)

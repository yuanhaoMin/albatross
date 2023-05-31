from langchain import OpenAI, SerpAPIWrapper
from langchain.agents import AgentType, Tool, initialize_agent
from service.setting_service import get_api_key_settings


def online_search(question):
    llm = OpenAI(
        model_name="text-davinci-003",
        temperature=0,
        max_tokens=1024,
        openai_api_key=get_api_key_settings().openai_api_key,
        request_timeout=2,
        max_retries=1,
        streaming=True,
    )
    search = SerpAPIWrapper(
        serpapi_api_key=get_api_key_settings().serper_api_key,
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
    output_data = agent.apply([question])
    final_answer = output_data[0]["output"]
    intermediate_steps = output_data[0]["intermediate_steps"]
    return (final_answer, intermediate_steps)

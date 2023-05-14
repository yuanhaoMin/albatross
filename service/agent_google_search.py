from config.constant import APIKey
from langchain import OpenAI, SerpAPIWrapper
from langchain.agents import AgentType, Tool, initialize_agent, load_tools
from langchain.callbacks import get_openai_callback


def run(question):
    # initialize llm
    llm = OpenAI(
        model_name="text-davinci-003",
        temperature=0,
        max_tokens=1024,
        openai_api_key=APIKey.OPENAI_API_KEY,
        request_timeout=2,
        max_retries=1,
        streaming=True,
    )
    search = SerpAPIWrapper(
        serpapi_api_key=APIKey.SERPER_API_KEY,
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

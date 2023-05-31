import httpx
import json
from concurrent.futures import ThreadPoolExecutor


def test_endpoint(url):
    with httpx.stream("GET", url) as r:
        for chunk in r.iter_raw():
            json_data = json.loads(chunk)  # Parse the JSON string
            print(json_data)


local_base_url = "http://127.0.0.1:8000"
completion_stream_url = (
    local_base_url + "/llm/openai/completion-stream?username=user&test_mode=false"
)

test_endpoint(completion_stream_url)

# # Define the URLs
# urls = [
#     "http://127.0.0.1:8000/completion/message-stream?username=fakeuser",
#     "http://127.0.0.1:8000/completion/message-stream?username=fakeuser",
#     "http://127.0.0.1:8000/completion/message-stream?username=fakeuser",
#     "http://127.0.0.1:8000/completion/message-stream?username=fakeuser",
# ]

# # Create a ThreadPoolExecutor with a maximum of 4 threads
# executor = ThreadPoolExecutor(max_workers=4)

# # Submit each URL to the executor
# futures = [executor.submit(test_endpoint, url) for url in urls]

# # Wait for all futures to complete
# for future in futures:
#     future.result()

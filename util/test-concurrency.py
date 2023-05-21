import httpx
import json
from concurrent.futures import ThreadPoolExecutor


def test_endpoint(url):
    with httpx.stream("GET", url) as r:
        for chunk in r.iter_raw():
            json_data = json.loads(chunk.decode())  # Parse the JSON string
            data = json_data["data"]  # Access the "data" field
            print(data)


# Define the URLs
urls = [
    "http://127.0.0.1:8000/completion/message-stream?username=fakeuser",
    "http://127.0.0.1:8000/completion/message-stream?username=fakeuser",
    "http://127.0.0.1:8000/completion/message-stream?username=fakeuser",
    "http://127.0.0.1:8000/completion/message-stream?username=fakeuser",
]

# Create a ThreadPoolExecutor with a maximum of 4 threads
executor = ThreadPoolExecutor(max_workers=4)

# Submit each URL to the executor
futures = [executor.submit(test_endpoint, url) for url in urls]

# Wait for all futures to complete
for future in futures:
    future.result()
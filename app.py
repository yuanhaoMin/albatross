# pip list --format=freeze > requirements.txt
import os
import sys
from io import StringIO
import service.agent_google_search as agent_google_search
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/")
def health_check():
    return "Server is up!"


@app.route("/check-env")
def check_env():
    app.logger.info("check env")
    example_env = os.getenv("OPENAI_API_KEY")
    return example_env[-4:]


@app.route("/agent-search", methods=["POST"])
def agent_search():
    question = request.json.get("question")
    if not question:
        return jsonify({"error": "question parameter not provided"}), 400
    # Capture standard output in a string buffer
    stdout_buffer = StringIO()
    sys.stdout = stdout_buffer
    output, cost, total_tokens, successful_requests = agent_google_search.run(question)
    # Restore the standard output and get the captured string
    sys.stdout = sys.__stdout__
    captured_stdout = stdout_buffer.getvalue()
    response_data = {
        "output": output,
        "metadata": {
            "cost": cost,
            "total_tokens": total_tokens,
            "successful_requests": successful_requests,
            "stdout": captured_stdout,
        },
    }
    return jsonify(response_data)

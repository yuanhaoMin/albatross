import requests
import datetime
from decimal import Decimal, getcontext


def convert_to_datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def calculate_text_cost(data):
    model_name = data["snapshot_id"]
    n_generated_tokens_total = data["n_generated_tokens_total"]
    n_context_tokens_total = data["n_context_tokens_total"]

    if model_name == "text-davinci:003":
        cost_per_token = Decimal(0.02) / Decimal(1000)
        cost = (
            Decimal(n_generated_tokens_total + n_context_tokens_total) * cost_per_token
        )
    elif "gpt-3.5-turbo" in model_name:
        cost_per_token = Decimal(0.002) / Decimal(1000)
        cost = (
            Decimal(n_generated_tokens_total + n_context_tokens_total) * cost_per_token
        )
    elif "gpt-4" in model_name:
        gpt4_cost_per_prompt_token = Decimal(0.03) / Decimal(1000)
        gpt4_cost_per_completion_token = Decimal(0.06) / Decimal(1000)
        cost = (
            Decimal(n_generated_tokens_total) * gpt4_cost_per_completion_token
            + Decimal(n_context_tokens_total) * gpt4_cost_per_prompt_token
        )
    return cost


def calculate_dalle_cost(data):
    image_size = data["image_size"]
    num_images = data["num_images"]

    cost_per_image = 0.0
    if image_size == "256x256":
        cost_per_image = Decimal(0.016)
    elif image_size == "512x512":
        cost_per_image = Decimal(0.018)
    elif image_size == "1024x1024":
        cost_per_image = Decimal(0.02)

    cost = cost_per_image * num_images
    return cost


def calculate_whisper_cost(data):
    return Decimal(0.006) * data["minutes"]


def check_usage(api_key, date, user_public_id):
    headers = {"Authorization": f"Bearer {api_key}"}
    url = "https://api.openai.com/v1/usage"

    # Parameters for API request
    params = {"date": date.strftime("%Y-%m-%d"), "user_public_id": user_public_id}

    # Send API request and get response
    response = requests.get(url, headers=headers, params=params).json()
    total_cost = Decimal(0)

    text_usage = response["data"]
    for data in text_usage:
        # Get the aggregation_timestamp field and convert it to datetime
        timestamp = data["aggregation_timestamp"]
        data["aggregation_timestamp"] = convert_to_datetime(timestamp)

        # Calculate the cost
        cost = calculate_text_cost(data)
        total_cost += cost
        print(data, cost)

    dalle_usage = response["dalle_api_data"]
    for data in dalle_usage:
        cost = calculate_dalle_cost(data)
        total_cost += cost
        print(data, cost)
    print(f"Total cost: {total_cost:.4f}")
    return total_cost


getcontext().prec = 4
org_cost = Decimal(0)
# API key owner must be org owner to check all members' usage
api_key = "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"
# Date for which to get usage data
date = datetime.date(2023, 5, 15)
# Albatross user public ID
org_cost += check_usage(api_key, date, "user-owzG9StDhqaaHYddikoOHqjC")
# Qiankun user
org_cost += check_usage(api_key, date, "user-z4zwcjTeaOclAl8IvR9JcJYl")
print(f"Total cost for org: {org_cost:.4f}")

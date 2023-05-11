import requests
import datetime
import json

# API key
api_key = "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"

# API headers
headers = {'Authorization': f'Bearer {api_key}'}

# API endpoint
url = 'https://api.openai.com/v1/usage'

# Date for which to get usage data
date = datetime.date(2023, 5, 6)

# Parameters for API request
params = {'date': date.strftime('%Y-%m-%d')}

# Send API request and get response
response = requests.get(url, headers=headers, params=params)
usage_data = response.json()['data']

# Loop through the usage_data array
for data in usage_data:
    # Get the aggregation_timestamp field and convert it to datetime
    timestamp = data["aggregation_timestamp"]
    dt = datetime.datetime.fromtimestamp(
        timestamp).strftime('%Y, %m, %d, %H, %M')
    # Replace the timestamp field with the datetime object
    data["aggregation_timestamp"] = dt
print(len(usage_data))

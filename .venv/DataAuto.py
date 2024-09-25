import requests
import json
import re

# OpenSearch connection details
url = "https://100.104.101.73:50513/wazuh-states-vulnerabilities-*/_search?scroll=1m&size=1000"
username = "xiotz"
password = "L@b4man1!"  # Replace with your actual password
headers = {"Content-Type": "application/json"}

# Extract index pattern from URL
index_pattern = re.search(r'/([^/]+)\*/_search', url).group(1)
filename = f"{index_pattern.replace('-', '_')}.json"

# The query for OpenSearch
query = {
    "query": {
        "bool": {
            "should": [
                {"match": {"vulnerability.severity": "High"}},
                {"match": {"vulnerability.severity": "Critical"}}
            ],
            "minimum_should_match": 1
        }
    }
}

# Send the request to OpenSearch
response = requests.get(url, auth=(username, password), headers=headers, json=query, verify=False)

# Ensure the request was successful
if response.status_code == 200:
    # Save the response to a JSON file with the dynamic filename
    save_path = f"C:/Users/S Shivamshi/Desktop/WebDevRepos/xiotz_report/.venv/{filename}"
    with open(save_path, "w") as file:
        json.dump(response.json(), file, indent=4)
    print(f"Data saved to {filename}")
else:
    print(f"Error: {response.status_code}, {response.text}")

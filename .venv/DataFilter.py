import json

# Load the JSON data from the file
file_path = r'C:\Users\S Shivamshi\Desktop\WebDevRepos\xiotz_report\.venv\CriticalLog.json'
with open(file_path) as file:
    data = json.load(file)

# Access the relevant hits
hits = data['hits']['hits']

# Function to print vulnerability details
def print_vulnerability(vulnerability):
    print(f"Vulnerability ID: {vulnerability['id']}")
    print(f"Description: {vulnerability['description']}")
    print(f"Severity: {vulnerability['severity']}")
    print(f"CVSS Base Score: {vulnerability['score']['base']}")
    print(f"Detected at: {vulnerability['detected_at']}")
    print(f"Reference: {vulnerability['reference']}")
    print("-" * 40)

# Function to filter by date
def filter_by_date():
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    print(f"\nVulnerabilities detected between {start_date} and {end_date}:\n")
    for entry in hits:
        detected_at = entry['_source']['vulnerability']['detected_at'][:10]  # Extract the date part
        if start_date <= detected_at <= end_date:
            print_vulnerability(entry['_source']['vulnerability'])

# Function to filter by severity
def filter_by_severity():
    severity_level = input("Enter severity level (e.g., Critical, High, Medium, Low): ")

    print(f"\nVulnerabilities with severity '{severity_level}':\n")
    for entry in hits:
        severity = entry['_source']['vulnerability']['severity']
        if severity == severity_level:
            print_vulnerability(entry['_source']['vulnerability'])

# Function to filter by vulnerability ID
def filter_by_vulnerability_id():
    vuln_id = input("Enter vulnerability ID (e.g., CVE-2023-35349): ")

    print(f"\nDetails for Vulnerability ID '{vuln_id}':\n")
    for entry in hits:
        vulnerability = entry['_source']['vulnerability']
        if vulnerability['id'] == vuln_id:
            print_vulnerability(vulnerability)

# Function to display filter options to the user
def filter_options():
    print("\nChoose a filter option:")
    print("1. Filter by detection date")
    print("2. Filter by severity level")
    print("3. Filter by vulnerability ID")
    choice = input("\nEnter your choice (1, 2, or 3): ")

    if choice == '1':
        filter_by_date()
    elif choice == '2':
        filter_by_severity()
    elif choice == '3':
        filter_by_vulnerability_id()
    else:
        print("Invalid choice. Please try again.")

# Start filtering process
filter_options()

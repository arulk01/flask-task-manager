import requests

BASE_URL = "http://127.0.0.1:5000"

# Register a user
register_data = {"username": "testuser", "password": "testpassword"}
requests.post(f"{BASE_URL}/register", json=register_data)

# Login to get the token
login_data = {"username": "testuser", "password": "testpassword"}
response = requests.post(f"{BASE_URL}/login", json=login_data)
token = response.json().get("access_token")

# Add a task
headers = {"Authorization": f"Bearer {token}"}
task_data = {"title": "Learn Flask", "description": "Study Flask framework"}
requests.post(f"{BASE_URL}/tasks", json=task_data, headers=headers)

# Get all tasks
response = requests.get(f"{BASE_URL}/tasks", headers=headers)
print(response.json())  # Output all tasks

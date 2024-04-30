import requests

url = 'http://127.0.0.1:5000/create-accounts'
data = [
  {"email": "buyer1@example.com", "first_name": "John", "last_name": "Doe", "password": "Password", "role_id": 2},
  {"email": "buyer2@example.com", "first_name": "Alice", "last_name": "Smith", "password": "Password", "role_id": 2},
  {"email": "buyer3@example.com", "first_name": "Michael", "last_name": "Johnson", "password": "Password", "role_id": 2},
  {"email": "buyer4@example.com", "first_name": "Emily", "last_name": "Brown", "password": "Password", "role_id": 2},
  {"email": "buyer5@example.com", "first_name": "Daniel", "last_name": "Wilson", "password": "Password", "role_id": 2},
  {"email": "seller1@example.com", "first_name": "Emma", "last_name": "Taylor", "password": "Password", "role_id": 2},
  {"email": "seller2@example.com", "first_name": "Christopher", "last_name": "Anderson", "password": "Password", "role_id": 2},
  {"email": "seller3@example.com", "first_name": "Olivia", "last_name": "Thomas", "password": "Password", "role_id": 2},
  {"email": "seller4@example.com", "first_name": "Matthew", "last_name": "Jackson", "password": "Password", "role_id": 2},
  {"email": "seller5@example.com", "first_name": "Sophia", "last_name": "White", "password": "Password", "role_id": 2},
  {"email": "agent1@example.com", "first_name": "David", "last_name": "Clark", "password": "Password", "role_id": 3, "cea_registration_no": "CEA0001", "agency_license_no": "AGC001"},
  {"email": "agent2@example.com", "first_name": "Sarah", "last_name": "Martinez", "password": "Password", "role_id": 3, "cea_registration_no": "CEA0002", "agency_license_no": "AGC002"},
  {"email": "agent3@example.com", "first_name": "Michael", "last_name": "Hernandez", "password": "Password", "role_id": 3, "cea_registration_no": "CEA0003", "agency_license_no": "AGC003"},
  {"email": "agent4@example.com", "first_name": "Jennifer", "last_name": "Lopez", "password": "Password", "role_id": 3, "cea_registration_no": "CEA0004", "agency_license_no": "AGC004"},
  {"email": "agent5@example.com", "first_name": "James", "last_name": "Garcia", "password": "Password", "role_id": 3, "cea_registration_no": "CEA0005", "agency_license_no": "AGC005"}
]



response = requests.post(url, json=data)

print(response.json())
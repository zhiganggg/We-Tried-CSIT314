import requests
import random
from faker import Faker

fake = Faker(en')

# Define the URL for the signup endpoint
createlisting_url = 'http://127.0.0.1:5000/create-listing'

# Define the payload data for the signup form
payload = {
    'type': 'HDB'
}

# Define the number of accounts to register
num_accounts = 25

location = fake.address()

# Loop to register multiple accounts
for i in range(1, num_accounts+1):
    payload['title'] = f'Listing {i}'  # Set unique last name
    payload['description'] = f'description {i}'
    payload['price'] = str(random.randint(500000, 3000000))
    payload['bedrooms'] = str(random.randint(1, 6))
    payload['bathrooms'] = str(random.randint(1, 3))
    payload['size_sqft'] = str(random.randint(1000, 2000))
    payload['location'] = location
    payload['photo'] = f'./media/hdb{i}.jpg'
    payload['user_email'] = f'seller{i}@example.com'
    payload['agent_id'] = f'{i}'
    response = requests.post(createlisting_url, data=payload)
    if response.status_code == 200:
        print(f'Account {i} registered successfully.')
    else:
        print(f'Error registering account {i}: {response.text}')

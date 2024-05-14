import requests

# Define the URL for the signup endpoint
signup_url = 'http://127.0.0.1:5000/sign-up'

# Define the payload data for the signup form
payload = {
    'first_name': 'Test',
    'password': 'Password',
    'verify_password': 'Password',
    'profile': '3',  # Assuming profile ID 1 corresponds to a specific user profile
}

# Define the number of accounts to register
num_accounts = 33

# Loop to register multiple accounts
for i in range(1, num_accounts+1):
    payload['last_name'] = f'Agent{i}'  # Set unique last name
    payload['email'] = f'agent{i}@example.com'  # Set email address based on the pattern
    payload['cea_registration_no'] = f'CEA{str(i).zfill(3)}'  # Zero-pad the number to three digits
    payload['agency_license_no'] = f'AGC{str(i).zfill(3)}'  # Zero-pad the number to three digits
    response = requests.post(signup_url, data=payload)
    if response.status_code == 200:
        print(f'Account {i} registered successfully.')
    else:
        print(f'Error registering account {i}: {response.text}')

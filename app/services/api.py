import requests
import os
from dotenv import load_dotenv
from app.utils import set_env_variable, get_env_variable
import csv
from app import config
import aiohttp
import asyncio



load_dotenv()
API_URL = f"{config.GET_EMPLOYE_URL}?pageSize=1000"


token_url = config.TOKEN_URL
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

async def getToken():
    data = {
        'grant_type': 'client_credentials',
        'scope': 'apiclients'            
    }
    try:
        access_token_response = requests.post(
            token_url,
            data=data,
            verify=False,
            allow_redirects=False,
            auth=(client_id, client_secret)
        )
        access_token_response.raise_for_status()

        tokens = access_token_response.json()
        set_env_variable('token',tokens["access_token"]
)
        return tokens
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération du token: {e}")
        if access_token_response is not None:
            print("Response content:", access_token_response.text)
        exit(1)

async def appelerEmployes():
    client_id = os.getenv('CLIENT_ID')
    token = await getToken()
    if not client_id:
        raise ValueError("CLIENT_ID est introuvable")

    headers = {
        "Authorization": f"Bearer {token['access_token']}",
        "X-IBM-Client-Id": client_id
    }
    try:
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()        
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        exit()

async def appelerClient(url):
    client_id = os.getenv('CLIENT_ID')
    token = await getToken()
    if not client_id:
        raise ValueError("CLIENT_ID est introuvable")

    headers = {
        "Authorization": f"Bearer {token['access_token']}",
        "X-IBM-Client-Id": client_id
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()        
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error while making API call: {e}")
        exit()
    return

async def appelerPlusieursClients(listeUrl=[]):
    client_id = os.getenv('CLIENT_ID')
    token = await getToken()
    if not client_id:
        raise ValueError("CLIENT_ID est introuvable")

    headers = {
        "Authorization": f"Bearer {token['access_token']}",
        "X-IBM-Client-Id": client_id
    }
    try:
        responses = []  # Initialize an empty list to store the responses
        async with aiohttp.ClientSession() as session:
            for url in listeUrl:
                async with session.get(url, headers=headers) as response:
                    response.raise_for_status()  # Raise an exception for HTTP errors
                    json_response = await response.json()  # Await the response JSON
                    responses.append(json_response)  # Append to the list

        return responses  # Return the collected responses
    except aiohttp.ClientError as e:  # Handle aiohttp-specific exceptions
        print(f"Error while making API call: {e}")
        exit()
    return

async def getC2Clients():

    api_url = config.GET_C2_CLIENTS_URL
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json-patch+json"
    }
    body = {
        "Page": 0,
        "Size": 10000,
        "SearchCriteria": {
            "ExcludeResources": False,
            "ExcludeMissingEmail": True,
            "IncludeCustomFields": False,
            "IncludeInactives": False
        },
        "UserName": username,
        "Password": password
    }

    response = requests.post(api_url, headers=headers, json=body)
    response.raise_for_status() 
    data = response.json().get('Data')
    emails = [record.get("EmailAddress") for record in data if "EmailAddress" in record]

    try:
        with open(config.C2_CLIENT_CSV, mode="w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["EmailAddress"])
            for email in emails:
                writer.writerow([email])
    except Exception as e:
        print(f"Une erreur est survenue lors de la sauvegarde du csv: {e}")

    return response.json().get('Data')


async def import_to_c2():

    url = config.IMPORT_TO_C2_URL
    file_path = config.DIFF_FILE_PATH
    delimiter = ','
    validation_only = 'false'

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    try:
        with open(file_path, 'rb') as file_stream:
            files = {
                'UploadFiles': (os.path.basename(file_path), file_stream, 'text/csv')
            }
            data = {
                'SearchType': '1',
                'Path': '',
                'ValidationOnly': validation_only,
                'SearchCulture': 'fr-CA',
                'Delimiter': delimiter,
                'OnErrorResumeNext': 'true',
                'FileCulture': '',
                'MultipleSeparator': '|',
                'DoNotSendActivateAccountNotification': 'false',
                'KeepSynchronized': 'true',
                'UserName': username,
                'Password': password
            }

            response = requests.post(url, files=files, data=data, timeout=5000)

            if response.ok:
                print(f"Success: {response.status_code}")
                print(response.text)
            else:
                print(f"Error: {response.status_code}")
                print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    finally:
        print("Importation complète")






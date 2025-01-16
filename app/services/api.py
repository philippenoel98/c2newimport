import requests
import os
from dotenv import load_dotenv
from app.utils import set_env_variable, get_env_variable
import csv
from app import config
import aiohttp
import asyncio
from app.services.logger import logger

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
        set_env_variable('token', tokens["access_token"])
        print("Token retrieved successfully.")
        logger.info("Token retrieved successfully.")
        return tokens
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving token: {e}")
        logger.error(f"Error retrieving token: {e}")
        if access_token_response is not None:
            print("Response content:", access_token_response.text)
            logger.error(f"Response content: {access_token_response.text}")
        exit(1)

async def appelerEmployes():
    client_id = os.getenv('CLIENT_ID')
    token = await getToken()
    if not client_id:
        raise ValueError("CLIENT_ID is missing")

    headers = {
        "Authorization": f"Bearer {token['access_token']}",
        "X-IBM-Client-Id": client_id
    }
    try:
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()        
        print("Employee API call successful.")
        logger.info("Employee API call successful.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making API call: {e}")
        logger.error(f"Error making API call: {e}")
        exit()

async def appelerClient(url):
    client_id = os.getenv('CLIENT_ID')
    token = await getToken()
    if not client_id:
        raise ValueError("CLIENT_ID is missing")

    headers = {
        "Authorization": f"Bearer {token['access_token']}",
        "X-IBM-Client-Id": client_id
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()        
        print("Client API call successful.")
        logger.info("Client API call successful.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making API call: {e}")
        logger.error(f"Error making API call: {e}")
        exit()

async def appelerPlusieursClients(listeUrl=[]):
    client_id = os.getenv('CLIENT_ID')
    token = await getToken()
    if not client_id:
        raise ValueError("CLIENT_ID is missing")

    headers = {
        "Authorization": f"Bearer {token['access_token']}",
        "X-IBM-Client-Id": client_id
    }
    try:
        responses = []  
        async with aiohttp.ClientSession() as session:
            for url in listeUrl:
                async with session.get(url, headers=headers) as response:
                    response.raise_for_status()  
                    json_response = await response.json()  
                    responses.append(json_response)  

        print("Multiple client API calls successful.")
        logger.info("Multiple client API calls successful.")
        return responses  # Return the collected responses
    except aiohttp.ClientError as e:  
        print(f"Error making multiple API calls: {e}")
        logger.error(f"Error making multiple API calls: {e}")
        exit()

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

    try:
        response = requests.post(api_url, headers=headers, json=body)
        response.raise_for_status() 
        data = response.json().get('Data')
        emails = [record.get("EmailAddress") for record in data if "EmailAddress" in record]

        with open(config.C2_CLIENT_CSV, mode="w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["EmailAddress"])
            for email in emails:
                writer.writerow([email])

        print(f"C2 clients saved to CSV: {config.C2_CLIENT_CSV}")
        logger.info(f"C2 clients saved to CSV: {config.C2_CLIENT_CSV}")
        return response.json().get('Data')
    except Exception as e:
        print(f"Error saving C2 clients to CSV: {e}")
        logger.error(f"Error saving C2 clients to CSV: {e}")

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
                print(f"Import success: {response.status_code}")
                print(response.text)
                logger.info(f"Import success: {response.status_code}, Response: {response.text}")
            else:
                print(f"Import failed: {response.status_code}")
                print(response.text)
                logger.error(f"Import failed: {response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed during import: {e}")
        logger.error(f"Request failed during import: {e}")
    finally:
        print("Importation completed.")
        logger.info("Importation completed.")

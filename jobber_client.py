import requests
import os
import json

def refresh_token():
    data = {
        "grant_type": "refresh_token",
        "refresh_token": os.environ.get("REFRESH_TOKEN"),
        "client_id": os.environ.get("CLIENT_ID"),
        "client_secret": os.environ.get("CLIENT_SECRET")
    }
    response = requests.post("https://api.getjobber.com/oauth/token", data=data)
    if response.ok:
        tokens = response.json()
        return tokens.get("access_token")
    raise Exception("Failed to refresh token: " + response.text)

def get_access_token():
    return os.environ.get("ACCESS_TOKEN") or refresh_token()

def get_jobber_data():
    access_token = get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    url = "https://api.getjobber.com/api/clients"
    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        access_token = refresh_token()
        headers["Authorization"] = f"Bearer {access_token}"
        response = requests.get(url, headers=headers)

    if response.ok:
        return response.json().get("clients", [])
    raise Exception(f"Jobber API error: {response.status_code} - {response.text}")

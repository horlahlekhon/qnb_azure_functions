import os
import requests
from azure.identity import ClientSecretCredential

SKU_ORDER = ["A1", "A2", "A3", "A4", "A5", "A6"]

def get_token():
    credential = ClientSecretCredential(
        tenant_id=os.environ["TENANT_ID"],
        client_id=os.environ["CLIENT_ID"],
        client_secret=os.environ["CLIENT_SECRET"]
    )
    return credential.get_token("https://management.azure.com/.default").token

def get_current_sku(token):
    capacity_url = _capacity_url()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    print("headers" , headers)
    res = requests.get(capacity_url, headers=headers)
    res.raise_for_status()
    return res.json()["sku"]["name"]

def scale_to(token, target_sku):
    capacity_url = _capacity_url()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    res = requests.put(capacity_url, headers=headers, json={"sku": {"name": target_sku}})
    res.raise_for_status()
    return res.status_code

def get_adjacent_sku(current_sku, direction):
    idx = SKU_ORDER.index(current_sku)
    if direction == "up" and idx < len(SKU_ORDER) - 1:
        return SKU_ORDER[idx + 1]
    elif direction == "down" and idx > 0:
        return SKU_ORDER[idx - 1]
    return current_sku

def _capacity_url():
    return (
        f"https://management.azure.com/subscriptions/{os.environ['SUBSCRIPTION_ID']}"
        f"/resourceGroups/{os.environ['RESOURCE_GROUP']}"
        f"/providers/Microsoft.PowerBIDedicated/capacities/{os.environ['CAPACITY_NAME']}"
        f"?api-version=2021-01-01"
    )
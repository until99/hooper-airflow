import requests
import os
from dotenv import load_dotenv
import msal

load_dotenv()


def get_powerbi_access_token(
    tenant_id: str,
    client_id: str,
    client_secret: str,
) -> str | None:
    print("Acquiring token using application flow (service principal)...")
    app_msal = msal.ConfidentialClientApplication(
        client_id=client_id,
        authority=f"https://login.microsoftonline.com/{tenant_id}",
        client_credential=client_secret,
        verify=False,
    )
    token_result = app_msal.acquire_token_for_client(
        scopes=["https://analysis.windows.net/powerbi/api/.default"]
    )

    if not token_result:
        return None

    if "access_token" in token_result:
        return token_result["access_token"]

    if "error" in token_result:
        print(f"Token acquisition error: {token_result.get('error')}")
        print(f"Error description: {token_result.get('error_description')}")

    return None


def refresh_powerbi_dataset(dataset_id: str, group_id: str) -> None:
    tenant_id = os.getenv("AZURE_TENANT_ID")
    client_id = os.getenv("AZURE_CLIENT_ID")
    client_secret = os.getenv("AZURE_CLIENT_SECRET")

    if not tenant_id or not client_id or not client_secret:
        raise ValueError("Missing required Azure environment variables")

    access_token = get_powerbi_access_token(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret,
    )

    if not access_token:
        raise ValueError(
            "Failed to acquire access token. Check your Azure AD app permissions and credentials."
        )

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    body = {
        "notifyOption": "NoNotification",
    }

    print(f"Attempting to refresh dataset {dataset_id} in workspace {group_id}")
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/refreshes"
    response = requests.post(
        url,
        headers=headers,
        json=body,
        verify=False,
    )

    if response.status_code == 202:
        print("Dataset refresh initiated successfully.")
    else:
        raise ValueError(
            f"Failed to initiate dataset refresh: {response.status_code} - {response.text}"
        )

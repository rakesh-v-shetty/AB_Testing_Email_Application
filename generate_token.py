import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# --- CONFIGURATION ---
# Define the SCOPES. If you change them, delete the token.json file.
# This scope gives read-only access to your Gmail.
# For more scopes, see: https://developers.google.com/gmail/api/auth/scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'
# --- END CONFIGURATION ---

def get_gmail_credentials():
    """
    Authenticates the user and gets the credentials for the Gmail API.
    If a valid token.json file exists, it's loaded.
    Otherwise, it initiates the OAuth 2.0 flow to create a new token.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_FILE):
        print(f"Loading credentials from existing file: {TOKEN_FILE}")
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Credentials have expired. Refreshing token...")
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing token: {e}")
                print("Could not refresh token. Please re-authorize.")
                creds = run_authorization_flow()
        else:
            print("No valid credentials found. Starting authorization flow...")
            creds = run_authorization_flow()

        # Save the credentials for the next run
        try:
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
            print(f"Credentials saved to {TOKEN_FILE}")
        except Exception as e:
            print(f"Error saving credentials to {TOKEN_FILE}: {e}")
            
    return creds

def run_authorization_flow():
    """
    Runs the OAuth 2.0 installed application flow to get user credentials.
    """
    # Check if the credentials.json file exists
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"Error: Credentials file not found at '{CREDENTIALS_FILE}'")
        print("Please download your credentials from the Google Cloud Console and place it in the same directory as this script.")
        return None

    # Create a flow instance to manage the authorization process.
    flow = InstalledAppFlow.from_client_secrets_file(
        CREDENTIALS_FILE, SCOPES)
    
    # run_local_server will start a temporary local web server to handle the
    # OAuth 2.0 redirect. It will automatically open the authorization URL
    # in the user's default web browser.
    print("A browser window will now open for you to log in and authorize the application.")
    print("Please complete the authorization in your browser.")
    
    try:
        creds = flow.run_local_server(port=0)
        return creds
    except Exception as e:
        print(f"Failed to run local server for authorization: {e}")
        return None


if __name__ == '__main__':
    print("--- Gmail API Token Generation Script ---")
    credentials = get_gmail_credentials()
    if credentials:
        print("\nSuccessfully created or loaded token.json!")
        print("You can now use this file in your application.")
    else:
        print("\nFailed to generate token.json. Please check the error messages above.")


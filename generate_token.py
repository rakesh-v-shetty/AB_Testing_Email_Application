import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# These are the exact SCOPES required by your app.py file.
# Using the same scopes ensures the generated token is compatible.
SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.readonly']

CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'

def generate_token():
    """
    Generates a token.json file by running the Google OAuth 2.0 flow.
    """
    creds = None
    
    # Check if credentials.json exists
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"Error: The credentials file ('{CREDENTIALS_FILE}') was not found in this directory.")
        print("Please download it from your Google Cloud Console and place it here.")
        return

    # If a token file already exists, this script has likely run successfully before.
    if os.path.exists(TOKEN_FILE):
        print(f"'{TOKEN_FILE}' already exists. If you need to re-authenticate, please delete it and run this script again.")
        return

    # Start the authentication flow
    try:
        print("Starting the Google OAuth 2.0 authentication flow...")
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        
        # run_local_server will automatically open a browser for you to log in
        # and authorize the application.
        creds = flow.run_local_server(port=0)
        print("Authentication successful. The browser tab can be closed.")

    except Exception as e:
        print(f"An error occurred during the authentication flow: {e}")
        return

    # Save the credentials to the token.json file
    if creds:
        try:
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
            print(f"Success! Your authentication details have been saved to '{TOKEN_FILE}'.")
            print("You can now run your main application.")
        except Exception as e:
            print(f"Failed to write the token file: {e}")

if __name__ == '__main__':
    generate_token()
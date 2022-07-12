import pickle
import os
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from google.auth.transport.requests import Request
from flask import current_app
from report_generator_service.proxy.google_api_proxy.google_api_helper import GoogleApiName, GoogleApiScpoes, GoogleApiVersion, GoogleApiMemeType

class GoogleApiProxy():

    @classmethod
    def download_google_sheet(cls, google_sheet_url: str):
        client_config = current_app.config.get('google-api')
        client_config["private_key"] = client_config.get("private_key").replace('\\n', '\n')
        drive_service = cls.get_service(client_config, GoogleApiName.DRIVE, GoogleApiVersion.API_VERSION_V3, GoogleApiScpoes.DRIVE_SCOPE)
        url_split = google_sheet_url.split("/")
        target_spreadsheet_id = url_split[-2]
        print(target_spreadsheet_id)
        byte_data = drive_service.files().export_media(
            fileId = target_spreadsheet_id,
            mimeType = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        ).execute()

        return byte_data

    @classmethod
    def upload_google_sheet():
        raise NotImplementedError

    def get_service(client_config, api_name, api_version, scopes):
        """Get a service that communicates to a Google API.

        Args:
            api_name: The name of the api to connect to.
            api_version: The api version to connect to.
            scopes: A list auth scopes to authorize for the application.
            key_file_location: The path to a valid service account JSON key file.

        Returns:
            A service that is connected to the specified API.
        """

        credentials = ServiceAccountCredentials.from_json_keyfile_dict(client_config, scopes)

        # Build the service object.
        service = build(api_name, api_version, credentials=credentials)

        return service

    def create_service(client_config, api_name, api_version, *scopes, prefix=''):
        API_SERVICE_NAME = api_name
        API_VERSION = api_version
        SCOPES = [scope for scope in scopes[0]]
        
        cred = None
        working_dir = os.getcwd()
        token_dir = 'token files'
        pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}{prefix}.pickle'

        ### Check if token dir exists first, if not, create the folder
        if not os.path.exists(os.path.join(working_dir, token_dir)):
            os.mkdir(os.path.join(working_dir, token_dir))

        if os.path.exists(os.path.join(working_dir, token_dir, pickle_file)):
            with open(os.path.join(working_dir, token_dir, pickle_file), 'rb') as token:
                cred = pickle.load(token)

        if not cred or not cred.valid:
            if cred and cred.expired and cred.refresh_token:
                cred.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
                cred = flow.run_local_server()

            with open(os.path.join(working_dir, token_dir, pickle_file), 'wb') as token:
                pickle.dump(cred, token)

        try:
            service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
            print(API_SERVICE_NAME, API_VERSION, 'service created successfully')
            return service
        except Exception as e:
            print(e)
            print(f'Failed to create service instance for {API_SERVICE_NAME}')
            os.remove(os.path.join(working_dir, token_dir, pickle_file))
            return None

    def convert_to_RFC_datetime(self, year=1900, month=1, day=1, hour=0, minute=0):
        dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
        return dt
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from flask import current_app

from report_generator_service.exceptions.api_exception import InvalidGoogleSheetUrlException
from report_generator_service.proxy.google_api_proxy.google_api_helper import GoogleApiName, GoogleApiScpoes, GoogleApiVersion, GoogleApiMemeType

class GoogleApiProxy():

    @classmethod
    def download_google_sheet(cls, google_sheet_url: str):
        client_config = current_app.config.get('google-api')
        client_config["private_key"] = client_config.get("private_key").replace('\\n', '\n')
        drive_service = cls.get_service(client_config, GoogleApiName.DRIVE, GoogleApiVersion.API_VERSION_V3, GoogleApiScpoes.DRIVE_SCOPE)
        url_split = google_sheet_url.split("/")
        if len(url_split) < 2:
            raise InvalidGoogleSheetUrlException()
        target_spreadsheet_id = url_split[-2]
        byte_data = drive_service.files().export_media(
            fileId = target_spreadsheet_id,
            mimeType = GoogleApiMemeType.SPREADSHEET
        ).execute()

        return byte_data

    @classmethod
    def upload_google_sheet():
        raise NotImplementedError

    def get_service(client_config, api_name: str, api_version: str, scopes: str):
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

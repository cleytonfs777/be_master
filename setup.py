import os.path
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv

load_dotenv()

class MyDrive():

    def __init__(self):
        # If modifying these scopes, delete the file token.json.
        SCOPES = ['https://www.googleapis.com/auth/drive']
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())


        self.service = build('drive', 'v3', credentials=self.creds)

    def list_files(self, id_path, page_size=100):

        # Call the Drive v3 API
        arr_itens = []
        arr_temp = []
        results = self.service.files().list(q=f"parents='{id_path}'",
                                            pageSize=page_size, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
        else:
            for item in items:
                arr_temp.append(item['name'])
                arr_temp.append(item['id'])
                arr_itens.append(arr_temp)
                arr_temp = []
                # print(u'{0} ({1})'.format(item['name'], item['id']))

        return arr_itens

    def upload_file(self, filename, path, folder_id):
        media = MediaFileUpload(os.path.join(path, filename))

        response = self.service.files().list(
            q=f"name='{filename}' and parents='{folder_id}'",
            spaces='drive',
            fields='nextPageToken, files(id, name)',
            pageToken=None).execute()
        if len(response['files']) == 0:
            file_metadata = {
                'name': filename,
                'parents': [folder_id]
            }
            file = self.service.files().create(
                body=file_metadata, media_body=media, fields='id').execute()
            print(f"A new file was created {file.get('id')}")

        else:
            for file in response.get('files', []):
                # Process change

                update_file = self.service.files().update(
                    fileId=file.get('id'),
                    media_body=media,
                ).execute()
                print(f'Updated File')

    def create_folder(self, nome, id_path):
        """ Create a folder and prints the folder ID
        Returns : Folder Id
        """
        try:
            # create gmail api client
            file_metadata = {
                'title': 'Invoices',
                'mimeType': 'application/vnd.google-apps.folder',
                'name': nome,
                'parents': [id_path]

            }

            # pylint: disable=maybe-no-member
            file = self.service.files().create(body=file_metadata, fields='id'
                                        ).execute()
            print(f'Folder has created with ID: "{file.get("id")}".')

        except HttpError as error:
            print(F'An error occurred: {error}')
            file = None

        return file.get('id')

def main():
    # A pasta que contem todos os audion no caminho Meu Drive/FACULDADE/FORMAÇÃO SOCIO CULTURAL II/ARQUIVOS IV/2022
    pasta_main = os.getenv('ID_MAIN_DIR')
    my_drive = MyDrive()
    # my_drive.create_folder("Primeira", '1In4c6ohp23q5ln7gXWxUxKtwp-rK6eTH')
    caminho = os.getenv('ID_MAIN_WAY')
    files = os.listdir(caminho)
    print(files)
    # my_drive = MyDrive()
    # files = my_drive.list_files(pasta_main)
    # print(files)

    # fd_id = "4c6ohp23q5ln7gXWxUxKtwp"

    for item in files:
        my_drive.upload_file(item, caminho, pasta_main)


if __name__ == '__main__':
    main()

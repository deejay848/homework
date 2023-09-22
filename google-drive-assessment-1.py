from __future__ import print_function
from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

source_folder_id = '1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V'  
file_count = 0  
folder_count = 0 
SCOPES = 'https://www.googleapis.com/auth/drive.readonly.metadata'
store = file.Storage('storage.json')
creds = store.get()

if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_id_readonly.json', SCOPES)
    creds = tools.run_flow(flow, store)

#call Drive v3 API 
DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))

try:
    files = DRIVE.files().list(q="'{}' in parents".format(source_folder_id), fields="files(id, mimeType, name, parents)").execute().get('files', [])  

    if not files:
        print('The folder is empty.')

    else:
        print('\nSource folder ID: ' + source_folder_id)
       
        for file in files:

            if 'parents' in file:
                if file['mimeType'] == "application/vnd.google-apps.folder":
                    folder_count += 1
                
                else:
                    file_count += 1   
        
        print('\nNumber of folders:', folder_count) 
        print('Number of files:', file_count)

except Exception as e:
    print(e)
    exit()

from __future__ import print_function  
from googleapiclient import discovery  
from httplib2 import Http  
from oauth2client import file, client, tools  

SCOPES = 'https://www.googleapis.com/auth/drive'

source_folder_id = '1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V'  
destination_folder_id = '1pKENxxLDbUx5oEFPAeryh1HcGrEK2XzH'
store = file.Storage('storage1.json')  
creds = store.get()  
  
if not creds or creds.invalid:  
    flow = client.flow_from_clientsecrets('client_id_rw.json', SCOPES)  
    creds = tools.run_flow(flow, store)  
  
DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))  
  
def copy_folder( source_folder_id, destination_folder_id):  
    try:
        source_folder_files = DRIVE.files().get(fileId=source_folder_id).execute()

        new_folder_name = source_folder_files['name']  
    
        # Create a new folder under destination_folder_id  
        new_folder_metadata = {  
            'name': new_folder_name,  
            'mimeType': 'application/vnd.google-apps.folder',  
            'parents': [destination_folder_id]  
        }  
        new_folder = DRIVE.files().create(body=new_folder_metadata).execute()  
    
        # Query the children of source_folder_id  
        children_files = DRIVE.files().list(q="'{}' in parents".format(source_folder_id)).execute()

        for file in children_files['files']:  
            # If the file is a folder call copy_folder function, else copy file  
            if file['mimeType'] == 'application/vnd.google-apps.folder':  
                copy_folder(file['id'], new_folder['id'])  
            else:  
                new_file_metadata = {  
                    'name': file['name'],  
                    'parents': [new_folder['id']]  
                }  
                DRIVE.files().copy(fileId=file['id'], body=new_file_metadata).execute() 
    
    except Exception as e:
        print(e)
        exit()

print('\nCopying the contents(nested files/folders)\n\nFROM: ' + source_folder_id + '\nTO: ' + destination_folder_id) 
copy_folder( source_folder_id, destination_folder_id)
print('\nCopy complete.')

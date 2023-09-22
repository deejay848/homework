from __future__ import print_function  
from googleapiclient import discovery  
from httplib2 import Http  
from oauth2client import file, client, tools  

source_folder_id = '1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V'
total_folder_count=0
SCOPES = 'https://www.googleapis.com/auth/drive.readonly.metadata'  
store = file.Storage('storage.json')  
creds = store.get()  
  
if not creds or creds.invalid:  
    flow = client.flow_from_clientsecrets('client_id_readonly.json', SCOPES)  
    creds = tools.run_flow(flow, store)  

#call Drive v3 API 
DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))  

def list_folders(parent_id):
    try:
        files = DRIVE.files().list(q="'{}' in parents".format(parent_id), fields="files(id, mimeType, name, parents)").execute().get('files', [])  

        global total_folder_count
        sub_folder_count = 0
        
        if not files:  
            sub_folder_count = 0
    
        else:  
            for file in files:  
                
                if file['mimeType'] == 'application/vnd.google-apps.folder':
                    sub_folder_count += 1
                    total_folder_count +=1
                    list_folders(file['id'])
                    
        print('Top level folder ' + parent_id + ': ' + str(sub_folder_count)) 

    except Exception as e:
        print(e)
        exit()


print('\nBreakdown of top level folders count on source folder id ' + source_folder_id) 
list_folders(source_folder_id) 
print('\nTotal count of folders (incuding nested folders) on source folder id ' + source_folder_id + ': ' + str(total_folder_count))

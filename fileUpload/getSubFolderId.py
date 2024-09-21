def createGetSubfolder(service, parent_folder_id, subfolder_name):
    query = f"'{parent_folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder' and name = '{subfolder_name}'"
    results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    files = results.get('files', [])
    
    # If subfolder exists, return its ID, otherwise create it
    if files:
        return files[0]['id']
    
    # Create subfolder
    file_metadata = {
        'name': subfolder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_folder_id]
    }
    subfolder = service.files().create(body=file_metadata, fields='id').execute()
    return subfolder.get('id')
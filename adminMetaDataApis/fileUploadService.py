from . allowedMime import allowedTypes
import random, time
from fileUpload.uploadFile import uploadFileToDrive
def uploadMetaFiles(files):
  try:
   for file in files:
      if files[file] is None:
         return {"error":f"{file}  is required field", "status":False}, 400
      if files[file].content_type not in allowedTypes:
         return {"error":f"Invalid file type for {file}", "status":False}, 400
   docUrls={}   
   for file in files:
     fileName = f"{file}_{random.randint(0, 5)}_{int(time.time())}"
     url, fileId = uploadFileToDrive(fileName, file, files[file])
     docUrls[file] = {"url":url, "fileId": fileId}

   return docUrls, 201  
       
  except Exception as e:
    return {"error":"An error occurd while uploading file"}, 500   


def updateMetaFiles(files):
  try:
   filterUpdateFiles = {}
   for updateFile in files:
     if files[updateFile] is not None and files[updateFile] != 'null' and files[updateFile] != 'undefined':
       filterUpdateFiles[updateFile] = files[updateFile]
   
   if not  filterUpdateFiles :
     return {"message":"No file to update"}, 200
   
   for file in filterUpdateFiles:
      if files[file].content_type not in allowedTypes:
         return {"error":f"Invalid file type for {file}", "status":False}, 400
      
   docUrls={}   
   for file in filterUpdateFiles:
     fileName = f"{file}_{random.randint(0, 5)}_{int(time.time())}"
     url, fileId = uploadFileToDrive(fileName, file, files[file])
     docUrls[file] = {"url":url, "fileId": fileId}

   return docUrls, 201  
       
  except Exception as e:
    return {"error":"An error occurd while uploading file"}, 500    
      
      
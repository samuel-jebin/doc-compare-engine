from azure.storage.blob import BlobServiceClient as bsc
from azure.ai.formrecognizer import DocumentAnalysisClient as dac
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

load_dotenv()

connectionString = os.getenv("BLOB_CONNECTION_STRING")
# container_name = "cursorystorage "
# blob_name = "data"
doc_endpoint = os.getenv("DOC_ENDPOINT")
doc_api_key = os.getenv("DOC_API")

def read_json_from_blob(container_name,json_file_name):
    
    blob_service_client = bsc.from_connection_string(connectionString)
    blob_client  = blob_service_client.get_blob_client(container=container_name,blob=json_file_name )
    blob_byte = blob_client.download_blob().readall()
    json_content = blob_byte.decode(encoding = "utf-8")
    # print(json_content)
    return json_content
    

def upload_json_to_blob(json_text,blob_name):
    
    try:
        blob_service_client = bsc.from_connection_string(connectionString)
        blob_container  = blob_service_client.get_container_client(container="cursorytech-json" )
    
        blob_client = blob_container.get_blob_client(blob_name)
        if blob_client.exists():
            blob_client.delete_blob()
            print("Deleted existing blob")
    
        blob_container.upload_blob(
            name = blob_name,
            data= json_text,
        
        )
    
        print("upladed new")
        return True
    except Exception as e:
        print("Error uploading")
        return False
    


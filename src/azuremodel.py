import os
import tempfile
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

class AzureModel:
    def __init__(self, connection_string=None, container_name=None):
        self.connection_string = "DefaultEndpointsProtocol=https;AccountName=storageaccount0409;AccountKey=Qd/MmaRrYCpKLrz3Pvt/ZfL21/ir8rzAsFNOu5mCOD8cj02Oxw7Pm64Hn2ItBWhnUi8GJi/UY0jk+AStRZz/NQ==;EndpointSuffix=core.windows.net"
        self.container_name = "container"

    def upload_file_to_blob(self, file, file_name):
        try:
            # Create a BlobServiceClient using the connection string
            blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)

            # Get a BlobClient for the container and file
            blob_client = blob_service_client.get_blob_client(container=self.container_name, blob=file_name)

            # Upload the file to the blob storage
            with file:
                blob_client.upload_blob(file)

            return True
        except Exception as e:
            # Handle any exceptions that may occur during file upload
            print(f"Error uploading file to blob: {e}")
            return False

    def read_file_from_blob(self, file_name):
        try:
            # Create a BlobServiceClient using the connection string
            blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)

            # Get a BlobClient for the container and file
            blob_client = blob_service_client.get_blob_client(container=self.container_name, blob=file_name)

            # Download the file from the blob storage
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                with open(temp_file.name, "wb") as file:
                    file.write(blob_client.download_blob().readall())
            
            # Return the file path of the downloaded file
            return temp_file.name
        except Exception as e:
            # Handle any exceptions that may occur during file download
            print(f"Error reading file from blob: {e}")
            return None
    

# def upload_to_azure_blob(file_path, container_name, blob_name):
#     try:
#         blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
#         container_client = blob_service_client.get_container_client(container_name)

#         with open(file_path, "rb") as data:
#             container_client.upload_blob(name=blob_name, data=data)

#         return True
#     except Exception as e:
#         st.error(f"Error uploading file to Azure Blob Storage: {str(e)}")
#         return False

    # # Function to fetch file from Azure Blob Storage
    # def fetch_from_azure_blob(blob_name):
    #     try:
    #         blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
    #         container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)

    #         with open(blob_name, "wb") as data:
    #             data.write(container_client.download_blob(blob_name).readall())

    #         return True
    #     except Exception as e:
    #         st.error(f"Error fetching file from Azure Blob Storage: {str(e)}")
    #         return False

import streamlit as st
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os

# Azure Blob Storage credentials
AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=storageaccount0409;AccountKey=Qd/MmaRrYCpKLrz3Pvt/ZfL21/ir8rzAsFNOu5mCOD8cj02Oxw7Pm64Hn2ItBWhnUi8GJi/UY0jk+AStRZz/NQ==;EndpointSuffix=core.windows.net"
AZURE_CONTAINER_NAME = "container"

# Function to upload file to Azure Blob Storage
def upload_to_azure_blob(file_path, container_name, blob_name):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(container_name)

        with open(file_path, "rb") as data:
            container_client.upload_blob(name=blob_name, data=data)

        return True
    except Exception as e:
        st.error(f"Error uploading file to Azure Blob Storage: {str(e)}")
        return False

def main():
    st.title("File Uploader to Azure Blob Storage")

    uploaded_file = st.file_uploader("Choose a file...", type=["txt", "pdf", "csv", "jpg", "png"])

    if uploaded_file is not None:
        file_name = uploaded_file.name
        st.write(f"Uploading file: {file_name} ...")
        
        # Temporary path to store the uploaded file
        temp_file_path = os.path.join(".", file_name)
        
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(uploaded_file.getbuffer())
        
        if upload_to_azure_blob(temp_file_path, AZURE_CONTAINER_NAME, file_name):
            st.success(f"File uploaded successfully to Azure Blob Storage: {file_name}")
        else:
            st.error("File upload failed.")
        
        # Delete the temporary file after uploading to Azure Blob Storage
        os.remove(temp_file_path)

if __name__ == "__main__":
    main()

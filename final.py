import asyncio
import streamlit as st
from azure.storage.blob import BlobServiceClient, ContainerClient
from codeinterpreterapi import CodeInterpreterSession, File
import os
import uuid

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

# Function to fetch file from Azure Blob Storage
def fetch_from_azure_blob(blob_name):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)

        with open(blob_name, "wb") as data:
            data.write(container_client.download_blob(blob_name).readall())

        return True
    except Exception as e:
        st.error(f"Error fetching file from Azure Blob Storage: {str(e)}")
        return False

async def get_images(prompt: str, files: list = None):
    if files is None:
        files = []

    # Fetch the content from Azure Blob Storage for files with a blob_name
    for file in files:
        if file.blob_name:
            await file.load_content_from_blob()

    with st.chat_message("user"):
        st.write(prompt)

    with st.spinner():
        async with CodeInterpreterSession(model='gpt-4-32k') as session:
            response = await session.generate_response(
                prompt,
                files=files
            )
            with st.chat_message("assistant"):
                st.write(response.content)

                for file in response.files:
                    if file.get_image() is not None:
                        st.image(file.get_image(), caption=prompt, use_column_width=True)

def main():
    st.title("Code Interpreter with Azure Blob Storage")

    # This will create a textbox where you can input text
    input_text = st.text_area("Write your prompt")

    # This will create a file uploader where you can choose multiple CSV files
    uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True, type=".csv")

    uploaded_files_list = []
    for uploaded_file in uploaded_files:
        # Create a unique blob name for each file using a timestamp and a random string
        unique_blob_name = f"{str(uuid.uuid4())}_{uploaded_file.name}"

        # Temporary path to store the uploaded file
        temp_file_path = os.path.join(".", unique_blob_name)

        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(uploaded_file.getbuffer())

        if upload_to_azure_blob(temp_file_path, AZURE_CONTAINER_NAME, unique_blob_name):
            st.success(f"File uploaded successfully to Azure Blob Storage: {uploaded_file.name}")
            uploaded_files_list.append(File.from_blob_name(name=uploaded_file.name, blob_name=unique_blob_name))
        else:
            st.error("File upload failed.")

        # Delete the temporary file after uploading to Azure Blob Storage
        os.remove(temp_file_path)

    # This will create a button
    button_pressed = st.button('Run code interpreter', use_container_width=True)

    # This will display the image only when the button is pressed
    if button_pressed and input_text != "":
        with st.chat_message("user"):
            st.write(input_text)

        with st.spinner():
            asyncio.run(get_images(input_text, files=uploaded_files_list))

if __name__ == "__main__":
    main()

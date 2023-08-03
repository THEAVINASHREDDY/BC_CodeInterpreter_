import azure.functions as func
import logging
from codeinterpreterapi import CodeInterpreterSession
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Add your Azure Blob storage related methods here
class AzureModel:
    def upload_file_to_blob(self, filename, file_content):
        blob_service_client = BlobServiceClient.from_connection_string('your_connection_string')
        container_client = blob_service_client.get_container_client('your_container_name')
        blob_client = container_client.get_blob_client(filename)

        # Upload the file content to Blob storage
        blob_client.upload_blob(file_content, overwrite=True)

    def fetch_file_from_blob(self, filename):
        blob_service_client = BlobServiceClient.from_connection_string('your_connection_string')
        container_client = blob_service_client.get_container_client('your_container_name')
        blob_client = container_client.get_blob_client(filename)

        # Download the blob content
        file_content = blob_client.download_blob()
        return file_content.readall().decode('utf-8')

azure_model = AzureModel()

async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        logging.error("HTTP request does not contain valid JSON data")
        return func.HttpResponse("Bad Request: Invalid JSON data in the request body", status_code=400)

    logging.info(f"req_body: {req_body}")

    prompt = req_body.get('prompt')
    logging.info(f"prompt from request body: {prompt}")

    req_files = req.files

    file_names = []
    if 'file' in req_files:
        for file_name, file in req_files.items():
            file_content = file.read().decode('utf-8')
            logging.info(f"File Content for {file_name}: {file_content}")

            # Call the method from the 'AzureModel' class to upload the file to Blob storage.
            azure_model.upload_file_to_blob(file_name, file_content)

            file_names.append(file_name)

    # Call the get_images function and await the result
    output = await get_images(prompt, file_names)

    return func.HttpResponse(f"Hello, {prompt}. This HTTP triggered function executed successfully. The output is {output}")

async def get_images(prompt: str, file_names: list = None):
    logging.info("get images function called")

    if file_names is None:
        file_names = []

    files = []
    # Fetch the content from Azure Blob Storage for files with the given file_names
    for file_name in file_names:
        # Replace this logic with your code to fetch the file content from Blob storage based on the file_name.
        file_content = azure_model.fetch_file_from_blob(file_name)

        # Append the file content to the 'files' list
        files.append(file_content)

    # Now you have the content of all files in the 'files' list
    # You can pass this list of file contents to the Code Interpreter API if needed.

    async with CodeInterpreterSession(model='gpt-3.5-turbo-16k') as session:
        response = await session.generate_response(
            prompt,
            files=files
        )
        output = response.content

    return output


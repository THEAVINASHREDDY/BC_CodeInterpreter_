# import azure.functions as func
# import os
# import tempfile
# from codeinterpreterapi import CodeInterpreterSession, File
# import logging

# # def main(req: func.HttpRequest) -> func.HttpResponse:
# #     # Get prompt input from the request body
# #     # prompt = req.form.get('prompt', '')
    
# #     # # Get the uploaded file, if any
# #     # file = req.files.get('file')
    
# #     # if file:
# #     #     # Save the uploaded file to a temporary location
# #     #     with tempfile.NamedTemporaryFile(delete=False) as temp_file:
# #     #         file_content = file.read()
# #     #         temp_file.write(file_content)
# #     #         temp_file.seek(0)
            
# #     #         # Process the uploaded file (e.g., analyze code)
# #     #         result = get_images(prompt, temp_file.name)
# #     # else:
# #     #     # Process prompt input only (e.g., analyze code)
# #     #     result = get_images(prompt, None)
# #     #  def main(req: func.HttpRequest) -> func.HttpResponse:
    

# #     name = req.params.get('name')
# #     if not name:
# #         try:
# #             req_body = req.get_json()
# #         except ValueError:
# #             pass
# #         else:
# #             name = req_body.get('name')

# #     if name:
# #         return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
# #     else:
# #         return func.HttpResponse(
# #              "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
# #              status_code=200
# #         )
        
#     # # Return the analysis result as an HTTP response
#     # return func.HttpResponse(result, mimetype='text/plain', status_code=200)

# # def analyze_code(prompt, file_path):
# #     # Implement your code interpretation logic here
# #     # You can use external code interpreter services or execute code using language-specific SDKs.
# #     # Be cautious when executing user-provided code to prevent security risks.

# #     # For example, a simple mock analysis result:
# #     result = f"Analysis result for prompt: {prompt}"
    
# #     if file_path:
# #         result += f"\nFile uploaded and saved to {file_path}"
    
# #     return result

# # Function to fetch file from Azure Blob Storage

# # async def get_images(prompt: str, files: list = None):
# #     if files is None:
# #         files = []

# #     # # Fetch the content from Azure Blob Storage for files with a blob_name
# #     # for file in files:
# #     #     if file.blob_name:
# #     #         await file.load_content_from_blob()

# #     # with st.chat_message("user"):
# #     #     st.write(prompt)

    
# #     async with CodeInterpreterSession(model='gpt-3.5-turbo-16k') as session:
# #         response = await session.generate_response(
# #             prompt,
# #             files=files
# #         )
# #         output = response.content
# #         # for file in response.files:
# #         #         if file.get_image() is not None:
# #         #             st.image(file.get_image(), caption=prompt, use_column_width=True)
# #     return output



# def main(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')

#     prompt = req.params.get('prompt')
#     logging.info(f"prompt from url {prompt}")
#     # if not prompt:
#     #     try:
#     #         req_body = req.get_json()
#     #     except ValueError:
#     #         pass
#     #     else:
#     #         prompt = req_body.get('prompt')

#     if prompt:
#         try:
#             get_images(prompt)
#             output = get_images(prompt)
#         except Exception as output:
#             logging.info(f"Error: {output}")


#         return func.HttpResponse(f"Hello, {prompt}. This HTTP triggered function executed successfully. The output is {output}")
    
#     else:
#         return func.HttpResponse(
#              "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
#              status_code=200
#         )
    


# async def get_images(prompt: str, files: list = None):
#     logging.info("get images function called")

#     if files is None:
#         files = []

#     # # Fetch the content from Azure Blob Storage for files with a blob_name
#     # for file in files:
#     #     if file.blob_name:
#     #         await file.load_content_from_blob()

#     # with st.chat_message("user"):
#     #     st.write(prompt)

    
#     async with CodeInterpreterSession(model='gpt-3.5-turbo-16k') as session:
#         response = await session.generate_response(
#             prompt,
#             files=files
#         )
#         output = response.content
#         logging.info(f"out put from code interpreter system")
#         logging.info(f"code interpreter final output: {output}")
#         # for file in response.files:
#         #         if file.get_image() is not None:
#         #             st.image(file.get_image(), caption=prompt, use_column_width=True)
#     return output





# import azure.functions as func
# import logging
# from codeinterpreterapi import CodeInterpreterSession

# from src.azuremodel import AzureModel
# azure_model = AzureModel()

# async def main(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')

#     req_body = req.get_json()
#     logging.info(f"req_body: {req_body}")

#     prompt = req_body.get('prompt')
#     logging.info(f"prompt from request body: {prompt}")

#     req_files = req.files

#     if 'file' in req_files:
#         file = req_files['file']

#         file_content = file.read().decode('utf-8')
#         logging.info(f"File Content: {file_content}")
#         print(file_content)



#     # print(f"req_body, {req_body}")
#     # print(f"req_files, {req_files}")
#     return func.HttpResponse("Completed")
#     # if prompt:
#     #     try:
#     #         # Call the get_images function and await the result
#     #         output = await get_images(prompt)
#     #         logging.info(f"code interpreter final output: {output}")

#     #         return func.HttpResponse(f"Hello, {prompt}. This HTTP triggered function executed successfully. The output is {output}")
#     #     except Exception as e:
#     #         logging.error(f"Error: {e}")
#     #         return func.HttpResponse(f"Error occurred: {e}", status_code=500)
#     # else:
#     #     return func.HttpResponse(
#     #          "This HTTP triggered function executed successfully. Pass a name in the query string for a personalized response.",
#     #          status_code=200
#     #     )
    
# async def get_images(prompt: str, files: list = None):
#     logging.info("get images function called")

#     if files is None:
#         files = []

#     async with CodeInterpreterSession(model='gpt-3.5-turbo-16k') as session:
#         response = await session.generate_response(
#             prompt,
#             files=files
#         )
#         output = response.content

#     return output



import azure.functions as func
import logging
from codeinterpreterapi import CodeInterpreterSession
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Add your Azure Blob storage related methods here
class AzureModel:
    def upload_file_to_blob(self, filename, file_content):
        blob_service_client = BlobServiceClient.from_connection_string('DefaultEndpointsProtocol=https;AccountName=storageaccount0409;AccountKey=Qd/MmaRrYCpKLrz3Pvt/ZfL21/ir8rzAsFNOu5mCOD8cj02Oxw7Pm64Hn2ItBWhnUi8GJi/UY0jk+AStRZz/NQ==;EndpointSuffix=core.windows.net')
        container_client = blob_service_client.get_container_client('container')
        blob_client = container_client.get_blob_client(filename)

        # Upload the file content to Blob storage
        blob_client.upload_blob(file_content, overwrite=True)

    def fetch_file_from_blob(self, filename):
        blob_service_client = BlobServiceClient.from_connection_string('DefaultEndpointsProtocol=https;AccountName=storageaccount0409;AccountKey=Qd/MmaRrYCpKLrz3Pvt/ZfL21/ir8rzAsFNOu5mCOD8cj02Oxw7Pm64Hn2ItBWhnUi8GJi/UY0jk+AStRZz/NQ==;EndpointSuffix=core.windows.net')
        container_client = blob_service_client.get_container_client('container')
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


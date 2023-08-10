import azure.functions as func
import os
import tempfile
from codeinterpreterapi import CodeInterpreterSession, File

def run(req: func.HttpRequest, outputBlob: func.Out[bytes]) -> func.HttpResponse:
    # Get prompt input from the request body
    prompt = req.form.get('prompt', '')
    
    # Get the uploaded file, if any
    file = req.files.get('file')
    
    if file:
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file_content = file.read()
            temp_file.write(file_content)
            temp_file.seek(0)
            
            # Process the uploaded file (e.g., analyze code)
            result = get_images(prompt, temp_file.name)
            
            # Save the analysis result to a Blob storage
            outputBlob.set(result.encode('utf-8'))
    else:
        # Process prompt input only (e.g., analyze code)
        result = get_images(prompt, None)
        
    # Return the analysis result as an HTTP response
    return func.HttpResponse(result, mimetype='text/plain', status_code=200)

# def analyze_code(prompt, file_path):
#     # Implement your code interpretation logic here
#     # You can use external code interpreter services or execute code using language-specific SDKs.
#     # Be cautious when executing user-provided code to prevent security risks.

#     # For example, a simple mock analysis result:
#     result = f"Analysis result for prompt: {prompt}"
    
#     if file_path:
#         result += f"\nFile uploaded and saved to {file_path}"
    
#     return result

# Function to fetch file from Azure Blob Storage

async def get_images(prompt: str, files: list = None):
    if files is None:
        files = []

    # # Fetch the content from Azure Blob Storage for files with a blob_name
    # for file in files:
    #     if file.blob_name:
    #         await file.load_content_from_blob()

    # with st.chat_message("user"):
    #     st.write(prompt)

    
    async with CodeInterpreterSession(model='gpt-3.5-turbo-16k') as session:
        response = await session.generate_response(
            prompt,
            files=files
        )
        output = response.content
        # for file in response.files:
        #         if file.get_image() is not None:
        #             st.image(file.get_image(), caption=prompt, use_column_width=True)
    return output
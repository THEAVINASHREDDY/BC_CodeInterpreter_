import asyncio
from pydantic import BaseModel


from azure.storage.blob import BlobServiceClient, ContainerClient

AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=storageaccount0409;AccountKey=Qd/MmaRrYCpKLrz3Pvt/ZfL21/ir8rzAsFNOu5mCOD8cj02Oxw7Pm64Hn2ItBWhnUi8GJi/UY0jk+AStRZz/NQ==;EndpointSuffix=core.windows.net"
AZURE_CONTAINER_NAME = "container"


class File(BaseModel):

    name: str
    content: bytes = None  # Make the content field optional
    blob_name: str = None
    

    @classmethod
    def from_bytes(cls, name: str, content: bytes):
        return cls(name=name, content=content)

    @classmethod
    def from_path(cls, path: str):
        with open(path, "rb") as f:
            path = path.split("/")[-1]
            return cls(name=path, content=f.read())

    @classmethod
    async def afrom_path(cls, path: str):
        return await asyncio.to_thread(cls.from_path, path)

    @classmethod
    def from_url(cls, url: str):
        import requests  # type: ignore

        r = requests.get(url)
        return cls(name=url.split("/")[-1], content=r.content)

    @classmethod
    async def afrom_url(cls, url: str):
        import aiohttp

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                return cls(name=url.split("/")[-1], content=await r.read())
            
    @classmethod
    def from_blob_name(cls, name: str, blob_name: str):
        return cls(name=name, blob_name=blob_name)
    
    async def load_content_from_blob(self):
        if self.blob_name:
            try:
                blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
                container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)
                blob = container_client.get_blob_client(self.blob_name)
                self.content = blob.download_blob().readall()
            except Exception as e:
                print(f"Error loading content from Azure Blob Storage: {str(e)}")
        else:
            print("Blob name is missing, cannot load content from Azure Blob Storage")

    def save(self, path: str):
        with open(path, "wb") as f:
            f.write(self.content)

    async def asave(self, path: str):
        await asyncio.to_thread(self.save, path)

    def get_image(self):
        try:
            from PIL import Image  # type: ignore
        except ImportError:
            print(
                "Please install it with `pip install codeinterpreterapi[image_support]` to display images."
            )
            exit(1)

        from io import BytesIO

        img_io = BytesIO(self.content)
        img = Image.open(img_io)

        # Convert image to RGB if it's not
        if img.mode not in ('RGB', 'L'):  # L is for greyscale images
            img = img.convert('RGB')

        return img

    def show_image(self):
        img = self.get_image()

        # Display the image
        try:
            # Try to get the IPython shell if available.
            shell = get_ipython().__class__.__name__  # type: ignore

            # If the shell is ZMQInteractiveShell, it means we're in a Jupyter notebook or similar.
            if shell == 'ZMQInteractiveShell':
                from IPython.display import display
                display(img)
            else:
                # We're not in a Jupyter notebook.
                img.show()
        except NameError:
            # We're probably not in an IPython environment, use PIL's show.
            img.show()



    def __str__(self):
        return self.name

    def __repr__(self):
        return f"File(name={self.name})"
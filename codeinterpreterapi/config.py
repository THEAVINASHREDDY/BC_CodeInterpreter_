from pydantic import BaseSettings
from dotenv import load_dotenv
from typing import Optional
import openai
import os

# .env file
load_dotenv(".env")


class CodeInterpreterAPISettings(BaseSettings):
    """
    CodeInterpreter API Config
    """

    VERBOSE: bool = False

    CODEBOX_API_KEY: Optional[str] = None
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY_BC")
    print("config", OPENAI_API_KEY)
    openai.api_key = os.getenv("OPENAI_API_KEY_BC")
    openai.api_type = "azure"
    openai.api_version = "2023-03-15-preview"
    openai.api_base = os.getenv("OPENAI_ENDPOINT")
    print("config", openai.api_base)


settings = CodeInterpreterAPISettings()

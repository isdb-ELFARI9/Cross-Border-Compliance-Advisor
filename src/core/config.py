import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "YOUR_DEFAULT_KEY_HERE_IF_NOT_IN_ENV")
    PINECONE_ENVIRONMENT: str = os.getenv("PINECONE_ENVIRONMENT", "YOUR_DEFAULT_ENV_HERE_IF_NOT_IN_ENV")
    PINECONE_INDEX_FAS: str = os.getenv("PINECONE_INDEX_FAS", "YOUR_DEFAULT_INDEX_HERE_IF_NOT_IN_ENV")
    PINECONE_INDEX_SS: str = os.getenv("PINECONE_INDEX_SS", "YOUR_DEFAULT_INDEX_HERE_IF_NOT_IN_ENV")
    
    # Add other settings if needed

settings = Settings()




import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
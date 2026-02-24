# config.py
import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_SITE_URL = os.getenv("DEFAULT_SITE_URL")

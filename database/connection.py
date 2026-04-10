import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.getenv("DATABASE_URL")
key: str = os.getenv("DATABASE_KEY")
supabase: Client = create_client(url, key)
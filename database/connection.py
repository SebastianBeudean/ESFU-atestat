from supabase import create_client, Client
import streamlit as st

url: str = st.secrets["DATABASE_URL"]
key: str = st.secrets["DATABASE_KEY"]

supabase: Client = create_client(url, key)
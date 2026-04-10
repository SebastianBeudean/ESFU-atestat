import streamlit as st
from database.connection import supabase

utilizatori = (
    supabase.table("utilizatori")
    .select("*")
    .execute()
)

st.title("utilizatori")

st.dataframe(utilizatori.data)
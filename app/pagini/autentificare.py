import streamlit as st
import time
from database.connection import supabase

def verificare_email_parola(email, parola):
    rezultat = (
        supabase.table("utilizatori")
        .select("*")
        .eq("email", email)
        .execute()
    )

    if not rezultat.data:
        return None
    if rezultat.data[0]["parola"] != parola:
        return None

    rol = (
        supabase.table("roluri")
        .select("nume")
        .eq("id", rezultat.data[0]["rol_id"])
        .execute()
    )

    return rol.data[0]["nume"]

def autentificare():

    st.header("Autentificare și Înregistrare")
    st.divider()

    with st.form("form_autentificare"):
        email = st.text_input("Email")
        parola = st.text_input("Parolă", type="password")

        st.markdown("---")
        col1, col2 = st.columns([3, 0.9])

        login = col1.form_submit_button("Autentificare")
        signup = col2.form_submit_button("Înscriere Student")

    if login:
        rol = verificare_email_parola(email, parola)
        if rol:
            st.session_state.user = rol
            st.success("Autentificare realizată cu succes")
            time.sleep(1.5)

            if rol == "admin":
                st.session_state.pagina = "panou_general"
                st.rerun()
            else:
                st.session_state.pagina = "situatie_scolara"
                st.rerun()
        else:
            st.error("Email sau parola incorecte.")
    elif signup:
        st.session_state.pagina = "inscriere_student"
        st.rerun()
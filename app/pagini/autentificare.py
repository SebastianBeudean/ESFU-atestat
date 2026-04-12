import streamlit as st
import time
from app.pagini.functii.date_utilizatori import get_rol, get_userid

def autentificare():

    st.header("Autentificare și Înregistrare")
    st.divider()
    stanga, dreapta = st.columns([1, 1])
    with st.form("form_autentificare"):
        email = st.text_input("Email")
        parola = st.text_input("Parolă", type="password")

        st.markdown("---")
        col1, col2 = st.columns([4.5, 0.5])

        login = col1.form_submit_button("Autentificare")
        signup = col2.form_submit_button("Înscriere Student")

    if login:
        st.session_state.user_id = get_userid(email, parola)
        if st.session_state.user_id is not None:
            st.session_state.user_rol = get_rol()
            st.success("Autentificare realizată cu succes")
            time.sleep(0.5)

            if st.session_state.user_rol == "Admin":
                st.session_state.pagina = "Panou General"
                st.rerun()
            else:
                st.session_state.pagina = "Situație Școlară"
                st.rerun()
        else:
            st.error("Email sau parola incorecte.")
    elif signup:
        st.session_state.pagina = "Înscriere Student"
        st.rerun()
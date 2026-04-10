import streamlit as st
from app.pagini.autentificare import autentificare
from app.pagini.inscriere_student import inscriere_student
from app.pagini.panou_general import panou_general

###
if "user" not in st.session_state:
    st.session_state.user = "neautentificat"
if "pagina" not in st.session_state:
    st.session_state.pagina = "autentificare"
st.set_page_config(page_title = "ESFU", layout = "wide")

###
def router_pagini():
    if st.session_state.pagina == "autentificare":
        autentificare()
    elif st.session_state.pagina == "inscriere_student":
        inscriere_student()
    elif st.session_state.pagina == "panou_general":
        panou_general()
###
router_pagini()
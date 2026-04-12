import streamlit as st

from app.pagini.achitare_taxa_inscriere import achitare_taxa_inscriere
from app.pagini.autentificare import autentificare
from app.pagini.curriculum import curriculum
from app.pagini.finante import finante
from app.pagini.inscriere_student import inscriere_student
from app.pagini.panou_general import panou_general
from app.pagini.situatie_scolara import situatie_scolara
from app.pagini.studenti import studenti

###
if "user_rol" not in st.session_state:
    st.session_state.user_rol = "neautentificat"
if "pagina" not in st.session_state:
    st.session_state.pagina = "Autentificare"
if "user_id" not in st.session_state:
    st.session_state.user_id = None
st.set_page_config(page_title = "ESFU", layout = "wide")

###
def router_pagini():
    if st.session_state.pagina == "Autentificare":
        autentificare()
    elif st.session_state.pagina == "Înscriere Student":
        inscriere_student()
    elif st.session_state.pagina == "Panou General":
        panou_general()
    elif st.session_state.pagina == "Studenți":
        studenti()
    elif st.session_state.pagina == "Situație Școlară":
        situatie_scolara()
    elif st.session_state.pagina == "Curriculum":
        curriculum()
    elif st.session_state.pagina == "Achitare Taxă de Înscriere":
        achitare_taxa_inscriere()
    elif st.session_state.pagina == "Finanțe":
        finante()

###
router_pagini()
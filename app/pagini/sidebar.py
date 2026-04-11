import streamlit as st
from app.pagini.functii.date_utilizatori import get_numeprenume_utilizator_curent

def pagini_disponibile():
    if st.session_state.user_rol == "Admin":
        return ["Panou General", "Studenți", "Curriculum", "Finanțe"]
    else:
        return ["Situație Școlară", "Curriculum", "Achitare Taxă de Înscriere"]

def sidebar_navigare():
    st.sidebar.title("Navigare")

    pagini = pagini_disponibile()
    index_pagina = pagini.index(st.session_state.pagina)

    pagina_selectata = st.sidebar.selectbox(
        "Selectare Modul:",
        options=pagini,
        index=index_pagina
    )

    if pagina_selectata != st.session_state.pagina:
        st.session_state.pagina = pagina_selectata
        st.rerun()

    st.sidebar.divider()
    st.sidebar.text(get_numeprenume_utilizator_curent())
    st.sidebar.text(st.session_state.user_rol)

    if st.sidebar.button("Logout"):
        st.session_state.user_rol = "neautentificat"
        st.session_state.pagina = "Autentificare"
        st.rerun()
import streamlit as st

from app.pagini.functii.date_finante import get_plan_tarifar, get_salarii_profesori, get_situatie_achitare_inscriere, \
    get_incasari_achitate, get_incasari_neachitate, get_incasari_total, get_salarii_totale_cadre
from app.pagini.sidebar import sidebar_navigare

def finante():
    sidebar_navigare()
    st.header("Finanțe")
    st.divider()
    st.subheader("Situație Achitare Înscriere")

    st.dataframe(get_situatie_achitare_inscriere())

    st.subheader("Plan Tarifar")
    st.dataframe(get_plan_tarifar())

    st.subheader("Salarii profesori")
    st.dataframe(get_salarii_profesori())

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Încasări")
        status_transe = st.radio("Filtrare după statusul plății tranșelor", ["Toate", "Achitate", "Neachitate"], horizontal=True, key="status_transe_finante")
        if status_transe == "Achitate":
            valoare = get_incasari_achitate()
        elif status_transe == "Toate":
            valoare = get_incasari_total()
        elif status_transe == "Neachitate":
            valoare = get_incasari_neachitate()

        st.metric("Încasări", f"{valoare:.2f}")

    with col2:
        st.subheader("Cheltuieli")
        st.metric("Salarii totale cadre didactice", get_salarii_totale_cadre())
import streamlit as st
from app.pagini.functii.date_cursuri import nume_discipline, discipline_specializare, nume_specializari
from app.pagini.functii.date_utilizatori import get_examene_count
from app.pagini.sidebar import sidebar_navigare

def router_filtru_specializare_discipline(optiune):
    if optiune == "Toate":
        return nume_discipline()
    else:
        return discipline_specializare(optiune)

def panou_general():
    sidebar_navigare()
    st.header("Panou General")
    st.divider()
    st.subheader("Situație Școlară Studenți")

    col1, col2 = st.columns(2)
    specializare = col1.selectbox("Filtrare după specializare", options = ["Toate"] + nume_specializari() )
    disciplina = col2.selectbox("Filtrare după disciplină", options = ["Toate"] + router_filtru_specializare_discipline(specializare))

    stanga, dreapta = st.columns([1.2, 3])
    with stanga:
        col1, col2 = st.columns(2)
        col1.metric("Examene promovate", get_examene_count(specializare, disciplina, "promovate"))
        col2.metric("Restante", get_examene_count(specializare, disciplina, "restante"))

    st.subheader("Finanțe")
    perioada = st.radio("Filtrare după perioadă", ["12 luni", "6 luni", "1 lună"], horizontal = True)

    stanga, centru, dreapta, dreapta2 = st.columns([3, 1, 0.9, 0.2])
    with stanga:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Valoare totală tranșe achitate", 1)
        col2.metric("Valoare totală tranșe neachitate", 1)
        col3.metric("Valoarea tuturor tranșelor", 1)
        col4.metric("Valoare totală cheltuieli", 1)

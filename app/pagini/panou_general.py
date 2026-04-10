import streamlit as st
from app.pagini.functii.cursuri import nume_discipline, discipline_specializare, nume_specializari

def router_filtru_specializare_discipline(optiune):
    if optiune == "Toate":
        return nume_discipline()
    else:
        return discipline_specializare(optiune)

def panou_general():
    st.header("Panou General")
    st.divider()
    st.subheader("Situație Școlară Studenți")

    col1, col2 = st.columns(2)
    specializare = col1.selectbox("Filtrare după specializare", options = ["Toate"] + nume_specializari() )
    disciplina = col2.selectbox("Filtrare după disciplină", options = ["Toate"] + router_filtru_specializare_discipline(specializare))

    stanga, centru, dreapta = st.columns([2, 1.5, 1])
    with stanga:
        col1, col2, col3 = st.columns(3)
        col1.metric("Examene promovate", 1)
        col2.metric("Restante", 1)
        col3.metric("Examene ramase", 1)

    st.subheader("Finanțe")
    perioada = st.radio("Filtrare după perioadă", ["12 luni", "6 luni", "1 lună"], horizontal = True)

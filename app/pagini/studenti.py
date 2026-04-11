import streamlit as st
from app.pagini.functii.date_cursuri import nume_specializari, nume_discipline, discipline_specializare
from app.pagini.functii.date_utilizatori import get_date_generale_studenti, get_cnp_student, \
    get_date_generale_rezultate_examene
from app.pagini.sidebar import sidebar_navigare

def studenti():
    sidebar_navigare()
    st.header("Studenți")
    st.divider()

    st.subheader("Date Studenți")
    specializare_date_studenti = st.selectbox("Filtrare după specializare", ["Toate"] + nume_specializari(), key="specializare_date_studenti")

    st.dataframe(get_date_generale_studenti(specializare_date_studenti))

    st.subheader("Rezultate Examene")
    col1, col2, col3, col4 = st.columns(4)
    specializare_rezultate_examene = col1.selectbox("Filtrare după specializare", ["Toate"] + nume_specializari(), key="specializare_rezultate_examene")
    disciplina_rezultate_examene = col2.selectbox("Filtrare după disciplină", ["Toate"] + discipline_specializare(specializare_rezultate_examene), key="disciplina_rezultate_examene")
    nota_minima = col3.slider("Filtrare după nota minimă", 1, 10, 5, 1)
    cnp_student = col4.selectbox("Filtrare după CNP-ul studentului", ["Toți"] + get_cnp_student(specializare_rezultate_examene), key="cnp_student")

    st.dataframe(get_date_generale_rezultate_examene(specializare_rezultate_examene, disciplina_rezultate_examene, nota_minima, cnp_student))

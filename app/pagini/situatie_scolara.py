import streamlit as st
from app.pagini.functii.date_utilizatori import get_examene_count_situatiescolara, get_rezultate_situatiescolara, \
    adauga_nume_prenume_foaie
from app.pagini.functii.generatoare_CSV import foaie_matricola_to_csv, get_date_absolvent
from app.pagini.sidebar import sidebar_navigare

def situatie_scolara():
    sidebar_navigare()
    st.header("Situatie Școlară")
    st.subheader("Rezultate Examene")

    restante = get_examene_count_situatiescolara(tip="nepromovat")
    promovate = get_examene_count_situatiescolara(tip="promovat")
    col1, col2 = st.columns([1, 2])
    col1.metric("Examene Promovate", promovate)
    col2.metric("Restanțe", restante)

    date_foaie_matricola = get_rezultate_situatiescolara()
    st.dataframe(date_foaie_matricola)

    date_foaie_matricola = adauga_nume_prenume_foaie(date_foaie_matricola)
    date_foaie_matricola = foaie_matricola_to_csv(date_foaie_matricola)

    date_absolvent = get_date_absolvent()
    col1, col2 = st.columns([1, 2])
    with col1:
        st.download_button(
        "Descărcare foaie matricolă",
            data = date_foaie_matricola if date_foaie_matricola else "",
            file_name = f"foaie_matricola.csv",
            mime = "text/csv",
            disabled = not date_foaie_matricola
        )
    with col2:
        st.download_button(
            "Descărcare Diplomă Absolvent",
            data=date_absolvent if date_absolvent else "",
            file_name="diploma_absolvent.csv",
            mime="text/csv",
            disabled=(restante > 0 or not date_absolvent)
        )
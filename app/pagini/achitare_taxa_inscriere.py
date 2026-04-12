import streamlit as st
from app.pagini.functii.date_finante import get_transe_numar_student, get_transe_student, plateste_prima_transa_neachitata, get_transe_achitate_selectbox
from app.pagini.sidebar import sidebar_navigare
from app.pagini.functii.generatoare_CSV import genereaza_chitanta_csv

def achitare_taxa_inscriere():
    sidebar_navigare()
    st.header("Achitare Taxa Inscriere")
    st.divider()
    st.subheader("Tranșe")

    col1, col2 = st.columns(2)
    numar_achitate, numar_neachitate = get_transe_numar_student()
    col1.metric("Număr Tranșe Achitate", numar_achitate)
    col2.metric("Număr Tranșe Neachitate", numar_neachitate)

    st.dataframe(get_transe_student())

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Achită tranșa următoare")
        plata_online = st.button("Plătește online")
        if plata_online:
            if plateste_prima_transa_neachitata():
                st.success("Plată realizată cu succes.")
                st.rerun()
            else:
                st.info("Toate tranșele au fost deja achitate.")
    with col2:
        st.subheader("Descărcare chitanță")
        optiuni_chitanta = get_transe_achitate_selectbox()
        transa_selectata = st.selectbox("Selectare tranșă achitată", options=optiuni_chitanta if optiuni_chitanta else ["Nu există tranșe achitate"],key="transa_selectata", placeholder="Opțiuni")
        csv_data = genereaza_chitanta_csv(transa_selectata)
        st.download_button(
            "Descarcă",
            data=csv_data if csv_data else "",
            file_name=f"chitanta_transa_{transa_selectata}.csv",
            mime="text/csv",
            disabled=not csv_data
        )
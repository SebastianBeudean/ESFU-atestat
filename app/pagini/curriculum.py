import streamlit as st
from app.pagini.functii.date_cursuri import nume_specializari, get_curriculum_admin, get_curriculum_student
from app.pagini.sidebar import sidebar_navigare

def curriculum():
    sidebar_navigare()
    st.header("Curriculum")
    st.divider()

    if st.session_state.user_rol == "Admin":
        specializare = st.selectbox("Filtrare după specializare", options = ["Toate"] + nume_specializari(), key="specializari_curriculum")
        st.dataframe(get_curriculum_admin(specializare))
    else:
        st.dataframe(get_curriculum_student(st.session_state.user_id))
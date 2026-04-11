import datetime
import streamlit as st
import time
from app.pagini.functii.date_cursuri import nume_specializari
from database.connection import supabase

def creare_student(email, parola, cnp, data_nastere, specializare, numar_transe, nume, prenume):

    if(
        email is None or parola is None or cnp is None or data_nastere is None or
        specializare is None or nume is None or prenume is None
    ):
        return False

    utilizator = supabase.table("utilizatori").insert({
        "email": email,
        "parola": parola,
        "nume": nume,
        "prenume": prenume,
        "rol_id": 3
    }).execute()

    utilizator_id = utilizator.data[0]["id"]

    student = supabase.table("studenti").insert({
        "utilizator_id": utilizator_id,
        "cnp": cnp,
        "data_nastere": data_nastere.isoformat()
    }).execute()

    student_id = student.data[0]["id"]

    specializarea_aleasa = supabase.table("specializari").select("id").eq("nume", specializare).execute()
    specializare_id = specializarea_aleasa.data[0]["id"]

    supabase.table("fise_inscriere").insert({
        "student_id": student_id,
        "specializare_id": specializare_id,
        "numar_transe": numar_transe,
        "data_inscriere": datetime.datetime.now().isoformat(timespec="seconds"),
        "absolvent": False
    }).execute()

    return True

def inscriere_student():
    st.header("Înscriere Student")
    st.divider()

    with st.form("form_inscriere_student"):
        email = st.text_input("Email")
        parola = st.text_input("Parolă", type="password")
        prenume = st.text_input("Prenume")
        nume = st.text_input("Nume")
        cnp = st.text_input("CNP")
        data_nastere = st.date_input("Data nastere", format = "DD/MM/YYYY", min_value = datetime.date(1900, 1, 1))
        specializare = st.selectbox("Specializare", options= nume_specializari(), placeholder="Selectați specializarea dorită", index = None)
        numar_transe = st.slider("Număr de tranșe pentru achitarea taxei de înscriere", 1, 8, 1, 1 )

        col1, col2 = st.columns([3, 1.1])

        sign_up = col1.form_submit_button("Înscriere")
        login = col2.form_submit_button("Înapoi la autentificare")

    if sign_up:
        if creare_student(email, parola, cnp, data_nastere, specializare, numar_transe, nume, prenume):
            st.success("Înscriere realizată cu succes.")
            time.sleep(1.5)
            st.rerun()
        else:
            st.error("Toate câmpurile trebuie completate")
    elif login:
        st.session_state.pagina = "Autentificare"
        st.rerun()
from database.connection import supabase
import streamlit as st
import pandas as pd
from io import StringIO

def genereaza_chitanta_csv(transa_selectata):
    user_id = st.session_state.user_id

    studenti = supabase.table("studenti").select("id, utilizator_id, cnp").execute().data or []
    fise_inscriere = supabase.table("fise_inscriere").select("id, student_id").execute().data or []
    transe = supabase.table("transe").select(
        "fise_inscriere_id, numar_transa, valoare, achitata, data_achitare"
    ).execute().data or []

    student_id = None
    cnp = None

    for s in studenti:
        if s["utilizator_id"] == user_id:
            student_id = s["id"]
            cnp = s["cnp"]
            break

    if not student_id:
        return ""

    fise_ids = []
    for f in fise_inscriere:
        if f["student_id"] == student_id:
            fise_ids.append(f["id"])

    randuri = []

    for t in transe:
        if t["fise_inscriere_id"] not in fise_ids:
            continue

        if t["numar_transa"] != transa_selectata:
            continue

        randuri.append({
            "numar_transa": t["numar_transa"],
            "valoare": t["valoare"],
            "achitata": t["achitata"],
            "data_achitare": t["data_achitare"],
            "CNP": cnp
        })

    df = pd.DataFrame(randuri)

    output = StringIO()
    df.to_csv(output, index=False)
    return output.getvalue()

def foaie_matricola_to_csv(date_foaie_matricola):
    if not date_foaie_matricola:
        return ""

    df = pd.DataFrame(date_foaie_matricola)

    return df.to_csv(index=False)

def get_date_absolvent():
    user_id = st.session_state.user_id

    utilizatori = supabase.table("utilizatori").select("id, nume, prenume").execute().data or []
    studenti = supabase.table("studenti").select("id, utilizator_id").execute().data or []
    fise_inscriere = supabase.table("fise_inscriere").select("student_id, specializare_id, absolvent").execute().data or []
    specializari = supabase.table("specializari").select("id, nume").execute().data or []

    utilizator = None
    for u in utilizatori:
        if u["id"] == user_id:
            utilizator = u
            break

    if not utilizator:
        return ""

    student_id = None
    for s in studenti:
        if s["utilizator_id"] == user_id:
            student_id = s["id"]
            break

    if not student_id:
        return ""

    specializare_id = None
    absolvent = None
    for f in fise_inscriere:
        if f["student_id"] == student_id:
            specializare_id = f["specializare_id"]
            absolvent = f["absolvent"]
            break

    if not specializare_id:
        return ""

    specializare_nume = None
    for s in specializari:
        if s["id"] == specializare_id:
            specializare_nume = s["nume"]
            break

    if not specializare_nume:
        return ""

    rezultat = [{
        "Nume": utilizator["nume"],
        "Prenume": utilizator["prenume"],
        "Specializare": specializare_nume,
        "Absolvent": absolvent
    }]

    df = pd.DataFrame(rezultat)
    return df.to_csv(index=False)
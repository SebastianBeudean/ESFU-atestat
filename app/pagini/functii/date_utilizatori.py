import streamlit as st
from database.connection import supabase

def get_userid(email, parola):
    rezultat = (
        supabase.table("utilizatori")
        .select("*")
        .eq("email", email)
        .execute()
    )

    if not rezultat.data:
        return None
    if rezultat.data[0]["parola"] != parola:
        return None

    return rezultat.data[0]["id"]

def get_rol():
    rol_id_query = (
        supabase.table("utilizatori")
        .select("rol_id")
        .eq("id", st.session_state.user_id)
        .execute()
    )
    rol_id = rol_id_query.data[0]["rol_id"]

    rol_nume_query = (
        supabase.table("roluri")
        .select("nume")
        .eq("id", rol_id)
        .execute()
    )
    rol_nume = rol_nume_query.data[0]["nume"]

    return rol_nume

def get_numeprenume_utilizator_curent():
    nume_prenume_query = (
        supabase.table("utilizatori")
        .select("nume, prenume")
        .eq("id", st.session_state.user_id)
        .execute()
    )
    nume_prenume_rezultat = nume_prenume_query.data[0]

    nume_prenume = nume_prenume_rezultat["nume"] + " " + nume_prenume_rezultat["prenume"]
    return nume_prenume

def get_date_generale_studenti(specializarea_aleasa):
    studenti = (
        supabase.table("studenti")
        .select("id, utilizator_id, cnp, data_nastere")
        .execute().data or []
    )

    utilizatori = (
        supabase.table("utilizatori")
        .select("id, nume, prenume")
        .execute().data or []
    )

    fise_inscriere = (
        supabase.table("fise_inscriere")
        .select("student_id, specializare_id, data_inscriere")
        .execute().data or []
    )

    specializari = (
        supabase.table("specializari")
        .select("id, nume")
        .execute().data or []
    )

    utilizatori_dictionar = {}
    for u in utilizatori:
        utilizatori_dictionar[u["id"]] = u

    fise_inscriere_dictionar = {}
    for f in fise_inscriere:
        fise_inscriere_dictionar[f["student_id"]] = f

    specializari_dictionar = {}
    for s in specializari:
        specializari_dictionar[s["id"]] = s

    rezultat = []

    for student in studenti:
        utilizator = utilizatori_dictionar.get(student["utilizator_id"])
        fisa = fise_inscriere_dictionar.get(student["id"])
        specializare = specializari_dictionar.get(fisa["specializare_id"])

        if not utilizator or not fisa or not specializare:
            continue

        if specializarea_aleasa != "Toate":
            if specializare["nume"] != specializarea_aleasa:
                continue

        rezultat.append({
            "Prenume": utilizator["prenume"],
            "Nume": utilizator["nume"],
            "CNP": student["cnp"],
            "Data Naștere": student["data_nastere"],
            "Specializare": specializare["nume"],
            "Data înscrierii": fisa["data_inscriere"]
        })
        rezultat.sort(key = lambda coloana: coloana["Data înscrierii"], reverse = True)

    return rezultat

def get_cnp_student(specializare):
    rezultat = []

    if specializare == "Toate":
        cnp_student = supabase.table("studenti").select("cnp").execute().data
        for student in cnp_student:
            rezultat.append(student["cnp"])
        return rezultat

    id_specializare = supabase.table("specializari").select("id").eq("nume", specializare).execute().data
    id_student = supabase.table("fise_inscriere").select("student_id").eq("specializare_id", id_specializare[0]["id"]).execute().data

    for student in id_student:
        cnp_student = supabase.table("studenti").select("cnp").eq("id", student["student_id"]).execute().data
        rezultat.append(cnp_student[0]["cnp"])

    return rezultat

def get_date_generale_rezultate_examene(specializare_aleasa, disciplina_aleasa, nota_minima, cnp_selectat):
    studenti = (
        supabase.table("studenti")
        .select("id, utilizator_id, cnp")
        .execute().data or []
    )

    utilizatori = (
        supabase.table("utilizatori")
        .select("id, nume, prenume")
        .execute().data or []
    )

    fise_inscriere = (
        supabase.table("fise_inscriere")
        .select("student_id, specializare_id")
        .execute().data or []
    )

    specializari = (
        supabase.table("specializari")
        .select("id, nume")
        .execute().data or []
    )

    discipline = (
        supabase.table("discipline")
        .select("id, nume")
        .execute().data or []
    )

    examene = (
        supabase.table("examene")
        .select("id, disciplina_id, numar_examen, data_examen")
        .execute().data or []
    )

    rezultate_examene = (
        supabase.table("rezultate_examene")
        .select("student_id, examen_id, nota")
        .execute().data or []
    )

    utilizatori_dict = {}
    for u in utilizatori:
        utilizatori_dict[u["id"]] = u

    fise_dict = {}
    for f in fise_inscriere:
        fise_dict[f["student_id"]] = f

    specializari_dict = {}
    for s in specializari:
        specializari_dict[s["id"]] = s

    discipline_dict = {}
    for d in discipline:
        discipline_dict[d["id"]] = d

    examene_dict = {}
    for e in examene:
        examene_dict[e["id"]] = e

    rezultat = []

    for rez in rezultate_examene:
        student = None
        for s in studenti:
            if s["id"] == rez["student_id"]:
                student = s
                break

        if not student:
            continue

        if cnp_selectat != "Toți":
            if student["cnp"] != cnp_selectat:
                continue

        utilizator = utilizatori_dict.get(student["utilizator_id"])
        fisa = fise_dict.get(student["id"])

        if not utilizator or not fisa:
            continue

        specializare = specializari_dict.get(fisa["specializare_id"])
        if not specializare:
            continue

        if specializare_aleasa != "Toate":
            if specializare["nume"] != specializare_aleasa:
                continue

        examen = examene_dict.get(rez["examen_id"])
        if not examen:
            continue

        disciplina = discipline_dict.get(examen["disciplina_id"])
        if not disciplina:
            continue

        if disciplina_aleasa != "Toate":
            if disciplina["nume"] != disciplina_aleasa:
                continue

        if rez["nota"] is not None:
            if rez["nota"] < nota_minima:
                continue

        rezultat.append({
            "Specializare": specializare["nume"],
            "Disciplina": disciplina["nume"],
            "Număr examen": examen["numar_examen"],
            "Data examen": examen["data_examen"],
            "Prenume": utilizator["prenume"],
            "Nume": utilizator["nume"],
            "CNP": student["cnp"],
            "Nota": rez["nota"]
        })

    rezultat.sort(key=lambda x: x["Data examen"], reverse=True)

    return rezultat

def get_examene_count(specializare_aleasa, disciplina_aleasa, tip):
    studenti = supabase.table("studenti").select("id").execute().data or []
    fise_inscriere = supabase.table("fise_inscriere").select("student_id, specializare_id").execute().data or []
    specializari = supabase.table("specializari").select("id, nume").execute().data or []
    discipline = supabase.table("discipline").select("id, nume").execute().data or []
    examene = supabase.table("examene").select("id, disciplina_id").execute().data or []
    rezultate = supabase.table("rezultate_examene").select("student_id, examen_id, nota").execute().data or []

    fise_dict = {f["student_id"]: f for f in fise_inscriere}
    specializari_dict = {s["id"]: s for s in specializari}
    discipline_dict = {d["id"]: d for d in discipline}
    examene_dict = {e["id"]: e for e in examene}

    count = 0

    for r in rezultate:
        if r["nota"] is None:
            continue

        if tip == "promovate" and r["nota"] < 5:
            continue

        if tip == "restante" and r["nota"] >= 5:
            continue

        student = None
        for s in studenti:
            if s["id"] == r["student_id"]:
                student = s
                break
        if not student:
            continue

        fisa = fise_dict.get(student["id"])
        if not fisa:
            continue

        specializare = specializari_dict.get(fisa["specializare_id"])
        if not specializare:
            continue

        if specializare_aleasa != "Toate" and specializare["nume"] != specializare_aleasa:
            continue

        examen = examene_dict.get(r["examen_id"])
        if not examen:
            continue

        disciplina = discipline_dict.get(examen["disciplina_id"])
        if not disciplina:
            continue

        if disciplina_aleasa != "Toate" and disciplina["nume"] != disciplina_aleasa:
            continue

        count += 1

    return count

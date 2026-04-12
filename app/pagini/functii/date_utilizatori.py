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
    specializari_discipline = supabase.table("specializari_discipline").select("specializare_id, disciplina_id").execute().data or []

    specializari_dict = {s["id"]: s for s in specializari}
    discipline_dict = {d["id"]: d for d in discipline}
    examene_dict = {e["id"]: e for e in examene}

    fisa_student = {}
    for f in fise_inscriere:
        fisa_student[f["student_id"]] = f["specializare_id"]

    examene_pe_student = {}
    for r in rezultate:
        examene_pe_student.setdefault(r["student_id"], []).append(r)

    discipline_pe_specializare = {}
    for sd in specializari_discipline:
        discipline_pe_specializare.setdefault(sd["specializare_id"], set()).add(sd["disciplina_id"])

    examene_pe_disciplina = {}
    for e in examene:
        examene_pe_disciplina.setdefault(e["disciplina_id"], []).append(e["id"])

    count = 0

    for student in studenti:
        student_id = student["id"]

        spec_id = fisa_student.get(student_id)
        if not spec_id:
            continue

        if specializare_aleasa != "Toate":
            spec = specializari_dict.get(spec_id)
            if not spec or spec["nume"] != specializare_aleasa:
                continue

        discipline_spec = discipline_pe_specializare.get(spec_id, set())

        if disciplina_aleasa != "Toate":
            discipline_spec = {
                d_id for d_id in discipline_spec
                if discipline_dict.get(d_id, {}).get("nume") == disciplina_aleasa
            }

        examene_expected = set()
        for d_id in discipline_spec:
            for ex_id in examene_pe_disciplina.get(d_id, []):
                examene_expected.add(ex_id)

        rezultate_student = examene_pe_student.get(student_id, [])

        examene_date = set()
        promovate = 0
        restante = 0

        for r in rezultate_student:
            examen = examene_dict.get(r["examen_id"])
            if not examen:
                continue

            if examen["id"] not in examene_expected:
                continue

            examene_date.add(examen["id"])

            if r["nota"] is not None:
                if r["nota"] >= 5:
                    promovate += 1
                else:
                    restante += 1

        examene_nedate = len(examene_expected - examene_date)

        if tip == "promovate":
            count += promovate
        else:
            count += restante + examene_nedate

    return count

def get_examene_count_situatiescolara(tip):
    user_id = st.session_state.user_id

    studenti = supabase.table("studenti").select("id, utilizator_id").execute().data or []
    fise_inscriere = supabase.table("fise_inscriere").select("student_id, specializare_id").execute().data or []
    specializari_discipline = supabase.table("specializari_discipline").select("specializare_id, disciplina_id").execute().data or []
    examene = supabase.table("examene").select("id, disciplina_id").execute().data or []
    rezultate = supabase.table("rezultate_examene").select("student_id, examen_id, nota").execute().data or []

    student_id = None
    for s in studenti:
        if s["utilizator_id"] == user_id:
            student_id = s["id"]
            break

    if not student_id:
        return 0

    fisa_spec = None
    for f in fise_inscriere:
        if f["student_id"] == student_id:
            fisa_spec = f["specializare_id"]
            break

    if not fisa_spec:
        return 0

    discipline_spec = set()
    for sd in specializari_discipline:
        if sd["specializare_id"] == fisa_spec:
            discipline_spec.add(sd["disciplina_id"])

    examene_expected = set()
    for e in examene:
        if e["disciplina_id"] in discipline_spec:
            examene_expected.add(e["id"])

    rezultate_map = {}
    for r in rezultate:
        if r["student_id"] == student_id:
            rezultate_map[r["examen_id"]] = r["nota"]

    count = 0

    for examen_id in examene_expected:
        nota = rezultate_map.get(examen_id)

        if tip == "promovat":
            if nota is not None and nota >= 5:
                count += 1

        elif tip == "nepromovat":
            if nota is None or nota < 5:
                count += 1

    return count

def get_rezultate_situatiescolara():
    utilizator_id = st.session_state.user_id
    studenti = supabase.table("studenti").select("id, utilizator_id").execute().data or []
    examene = supabase.table("examene").select("id, disciplina_id, numar_examen, data_examen").execute().data or []
    discipline = supabase.table("discipline").select("id, nume").execute().data or []
    rezultate = supabase.table("rezultate_examene").select("student_id, examen_id, nota").execute().data or []

    student_id = None
    for s in studenti:
        if s["utilizator_id"] == utilizator_id:
            student_id = s["id"]
            break

    if not student_id:
        return []

    discipline_dict = {}
    for d in discipline:
        discipline_dict[d["id"]] = d["nume"]

    examene_dict = {}
    for e in examene:
        examene_dict[e["id"]] = e

    rezultat_student = []
    for r in rezultate:
        if r["student_id"] == student_id:
            rezultat_student.append(r)

    rezultat = []

    for r in rezultat_student:
        examen = examene_dict.get(r["examen_id"])
        if not examen:
            continue

        rezultat.append({
            "Disciplina": discipline_dict.get(examen["disciplina_id"]),
            "Număr examen": examen["numar_examen"],
            "Dată examen": examen["data_examen"],
            "Notă": r["nota"]
        })

    return rezultat

def adauga_nume_prenume_foaie(date_foaie_matricola):
    if not date_foaie_matricola:
        return []

    nume_prenume = get_numeprenume_utilizator_curent()

    rezultat = []
    for row in date_foaie_matricola:
        row_nou = dict(row)
        row_nou["Student"] = nume_prenume
        rezultat.append(row_nou)

    return rezultat


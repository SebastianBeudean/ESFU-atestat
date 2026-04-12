from database.connection import supabase
import streamlit as st
import datetime

def get_transe_numar_student():
    utilizator_id = st.session_state.user_id

    studenti = supabase.table("studenti").select("id, utilizator_id").execute().data or []
    fise_inscriere = supabase.table("fise_inscriere").select("id, student_id").execute().data or []
    transe = supabase.table("transe").select("fise_inscriere_id, achitata").execute().data or []

    student_id = None
    for s in studenti:
        if s["utilizator_id"] == utilizator_id:
            student_id = s["id"]
            break

    if not student_id:
        return 0, 0

    fise_id = []
    for f in fise_inscriere:
        if f["student_id"] == student_id:
            fise_id.append(f["id"])

    achitate = 0
    neachitate = 0

    for t in transe:
        if t["fise_inscriere_id"] not in fise_id:
            continue

        if t["achitata"]:
            achitate += 1
        else:
            neachitate += 1

    return achitate, neachitate

def get_transe_student():
    user_id = st.session_state.user_id

    studenti = supabase.table("studenti").select("id, utilizator_id").execute().data or []
    fise_inscriere = supabase.table("fise_inscriere").select("id, student_id").execute().data or []
    transe = supabase.table("transe").select("fise_inscriere_id, numar_transa, valoare, achitata").execute().data or []

    student_id = None
    for s in studenti:
        if s["utilizator_id"] == user_id:
            student_id = s["id"]
            break

    if not student_id:
        return []

    fise_ids = []
    for f in fise_inscriere:
        if f["student_id"] == student_id:
            fise_ids.append(f["id"])

    rezultat = []

    for t in transe:
        if t["fise_inscriere_id"] not in fise_ids:
            continue

        rezultat.append({
            "Nr tranșă": t["numar_transa"],
            "Valoare": t["valoare"],
            "Achitată": t["achitata"]
        })

    return rezultat

def plateste_prima_transa_neachitata():
    utilizator_id = st.session_state.user_id

    studenti = supabase.table("studenti").select("id, utilizator_id").execute().data or []
    fise_inscriere = supabase.table("fise_inscriere").select("id, student_id").execute().data or []
    transe = supabase.table("transe").select("id, fise_inscriere_id, numar_transa, achitata").execute().data or []

    student_id = None
    for s in studenti:
        if s["utilizator_id"] == utilizator_id:
            student_id = s["id"]
            break

    if not student_id:
        return False

    fise_id = []
    for f in fise_inscriere:
        if f["student_id"] == student_id:
            fise_id.append(f["id"])

    transe_student = []
    for t in transe:
        if t["fise_inscriere_id"] in fise_id:
            transe_student.append(t)

    transe_student.sort(key=lambda x: x["numar_transa"])

    for t in transe_student:
        if not t["achitata"]:
            supabase.table("transe").update({
                "achitata": True,
                "data_achitare": datetime.datetime.now().isoformat(timespec="seconds"),
            }).eq("id", t["id"]).execute()
            return True

    return False

def get_transe_achitate_selectbox():
    utilizator = st.session_state.user_id

    studenti = supabase.table("studenti").select("id, utilizator_id").execute().data or []
    fise_inscriere = supabase.table("fise_inscriere").select("id, student_id").execute().data or []
    transe = supabase.table("transe").select("fise_inscriere_id, numar_transa, achitata").execute().data or []

    student_id = None
    for s in studenti:
        if s["utilizator_id"] == utilizator:
            student_id = s["id"]
            break

    if not student_id:
        return []

    fise_id = []
    for f in fise_inscriere:
        if f["student_id"] == student_id:
            fise_id.append(f["id"])

    optiuni = []

    for t in transe:
        if t["fise_inscriere_id"] not in fise_id:
            continue
        if t["achitata"]:
            optiuni.append(t["numar_transa"])

    optiuni.sort()

    return optiuni

def get_plan_tarifar():
    grade = supabase.table("grade_didactice").select("id, nume").execute().data or []
    planuri = supabase.table("planuri_tarifare").select("grad_didactic_id, tarif_ora").execute().data or []

    salarii = {}
    for p in planuri:
        salarii[p["grad_didactic_id"]] = salarii.get(p["grad_didactic_id"], 0) + p["tarif_ora"]

    rezultat = []

    for g in grade:
        rezultat.append({
            "Nume grad didactic": g["nume"],
            "Salariu": salarii.get(g["id"], 0)
        })

    return rezultat

def get_salarii_profesori():
    cadre = supabase.table("cadre_didactice").select("id, prenume, nume, grad_didactic_id").execute().data or []
    discipline = supabase.table("discipline").select("id, nume").execute().data or []
    rel = supabase.table("cadre_didactice_discipline").select("cadru_didactic_id, disciplina_id, ore_alocate").execute().data or []
    grade = supabase.table("grade_didactice").select("id, nume").execute().data or []
    planuri = supabase.table("planuri_tarifare").select("grad_didactic_id, tarif_ora").execute().data or []

    discipline_dict = {d["id"]: d["nume"] for d in discipline}
    grade_dict = {g["id"]: g["nume"] for g in grade}
    tarif_dict = {p["grad_didactic_id"]: p["tarif_ora"] for p in planuri}

    # agregare pe profesor
    profesori = {}

    for r in rel:
        cid = r["cadru_didactic_id"]
        did = r["disciplina_id"]
        ore = r["ore_alocate"]

        if cid not in profesori:
            profesori[cid] = {
                "discipline": [],
                "ore_totale": 0
            }

        nume_disc = discipline_dict.get(did)
        if nume_disc:
            profesori[cid]["discipline"].append(nume_disc)

        profesori[cid]["ore_totale"] += ore

    rezultat = []

    for c in cadre:
        cid = c["id"]

        data = profesori.get(cid)
        if not data:
            continue

        grad_id = c["grad_didactic_id"]
        tarif = tarif_dict.get(grad_id, 0)

        rezultat.append({
            "Prenume cadru didactic": c["prenume"],
            "Nume cadru didactic": c["nume"],
            "Grad didactic": grade_dict.get(grad_id),
            "Discipline": ", ".join(sorted(set(data["discipline"]))),
            "Ore de curs": data["ore_totale"],
            "Salariu": data["ore_totale"] * tarif
        })

    return rezultat

def get_situatie_achitare_inscriere():
    studenti = supabase.table("studenti").select("id, utilizator_id, cnp").execute().data or []
    utilizatori = supabase.table("utilizatori").select("id, nume, prenume").execute().data or []
    fise = supabase.table("fise_inscriere").select("id, student_id, specializare_id, numar_transe").execute().data or []
    specializari = supabase.table("specializari").select("id, cost_specializare").execute().data or []
    transe = supabase.table("transe").select("fise_inscriere_id, valoare, achitata").execute().data or []

    utilizatori_dict = {u["id"]: u for u in utilizatori}
    fise_by_student = {f["student_id"]: f for f in fise}
    specializari_dict = {s["id"]: s for s in specializari}

    transe_by_fisa = {}
    for t in transe:
        fid = t["fise_inscriere_id"]
        if fid not in transe_by_fisa:
            transe_by_fisa[fid] = []
        transe_by_fisa[fid].append(t)

    rezultat = []

    for s in studenti:
        fisa = fise_by_student.get(s["id"])
        if not fisa:
            continue

        utilizator = utilizatori_dict.get(s["utilizator_id"])
        specializare = specializari_dict.get(fisa["specializare_id"])

        if not utilizator or not specializare:
            continue

        lista_transe = transe_by_fisa.get(fisa["id"], [])

        nr_total = len(lista_transe)
        nr_achitate = 0
        suma_achitata = 0

        for t in lista_transe:
            if t["achitata"]:
                nr_achitate += 1
                suma_achitata += t["valoare"] or 0

        rezultat.append({
            "CNP": s["cnp"],
            "Prenume": utilizator["prenume"],
            "Nume": utilizator["nume"],
            "Număr tranșe totale": nr_total,
            "Număr tranșe achitate": nr_achitate,
            "Valoare totală": specializare["cost_specializare"],
            "Valoare totală achitată": suma_achitata
        })

    return rezultat

def get_incasari_achitate():
    transe = supabase.table("transe").select("valoare, achitata").execute().data or []

    total = 0

    for t in transe:
        if t["achitata"] is not True:
            continue

        total += float(t.get("valoare") or 0)

    return total

def get_incasari_neachitate():
    transe = supabase.table("transe").select("valoare, achitata").execute().data or []

    total = 0

    for t in transe:
        if t["achitata"]:
            continue

        total += t.get("valoare") or 0

    return total

def get_incasari_total():
    transe = supabase.table("transe").select("valoare").execute().data or []

    return sum(t.get("valoare") or 0 for t in transe)

def get_salarii_totale_cadre():
    cadre = supabase.table("cadre_didactice").select("id, grad_didactic_id").execute().data or []
    rel = supabase.table("cadre_didactice_discipline").select("cadru_didactic_id, ore_alocate").execute().data or []
    planuri = supabase.table("planuri_tarifare").select("grad_didactic_id, tarif_ora").execute().data or []

    tarif_dict = {p["grad_didactic_id"]: p["tarif_ora"] for p in planuri}
    ore_prof = {}

    for r in rel:
        cid = r["cadru_didactic_id"]
        ore_prof[cid] = ore_prof.get(cid, 0) + r["ore_alocate"]

    total_salarii = 0

    for c in cadre:
        cid = c["id"]
        grad_id = c["grad_didactic_id"]

        ore = ore_prof.get(cid, 0)
        tarif = tarif_dict.get(grad_id, 0)

        total_salarii += ore * tarif

    return total_salarii
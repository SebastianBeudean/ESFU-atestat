from database.connection import supabase

def nume_specializari():
    rezultat = (
        supabase.table("specializari")
        .select("nume")
        .order("nume", desc=False)
        .execute()
    )
    specializare = []
    for element in rezultat.data:
        specializare.append(element["nume"])

    return specializare

def nume_discipline():
    discipline_query = (
        supabase.table("discipline")
        .select("nume")
        .order("nume", desc=False)
        .execute()
    )
    discipline_nume = []
    for element in discipline_query.data:
        discipline_nume.append(element["nume"])

    return discipline_nume

def discipline_specializare(nume_specializare):

    if nume_specializare == "Toate": return nume_discipline()

    specializare_query = (
        supabase.table("specializari")
        .select("id")
        .eq("nume", nume_specializare)
        .execute()
    )
    specializare_id = specializare_query.data[0]["id"]

    relatie = (
        supabase.table("specializari_discipline")
        .select("disciplina_id")
        .eq("specializare_id", specializare_id)
        .execute()
    )
    id_discipline = []
    for element in relatie.data:
        id_discipline.append(element["disciplina_id"])

    disciplina_query = (
        supabase.table("discipline")
        .select("nume")
        .in_("id", id_discipline)
        .execute()
    )

    discipline_nume = []
    for element in disciplina_query.data:
        discipline_nume.append(element["nume"])

    return discipline_nume

def get_curriculum_admin(specializare_aleasa):
    specializari = supabase.table("specializari").select("id, nume").execute().data or []
    discipline = supabase.table("discipline").select("id, nume, ore_curs, credite").execute().data or []
    examene = supabase.table("examene").select("id, disciplina_id").execute().data or []
    specializari_discipline = supabase.table("specializari_discipline").select("specializare_id, disciplina_id").execute().data or []

    examene_dict = {}
    for e in examene:
        examene_dict[e["disciplina_id"]] = examene_dict.get(e["disciplina_id"], 0) + 1

    specializari_dict = {s["id"]: s for s in specializari}

    rezultat = []

    for sd in specializari_discipline:
        disciplina = None
        for d in discipline:
            if d["id"] == sd["disciplina_id"]:
                disciplina = d
                break

        if not disciplina:
            continue

        numar_examene = examene_dict.get(disciplina["id"], 0)

        if specializare_aleasa != "Toate":
            specializare = specializari_dict.get(sd["specializare_id"])
            if not specializare or specializare["nume"] != specializare_aleasa:
                continue
            rezultat.append({
                "Specializare": specializare["nume"],
                "Disciplina": disciplina["nume"],
                "Ore curs": disciplina["ore_curs"],
                "Credite": disciplina["credite"],
                "Număr examene": numar_examene
            })
        else:
            specializare = specializari_dict.get(sd["specializare_id"])
            if not specializare:
                continue
            rezultat.append({
                "Specializare": specializare["nume"],
                "Disciplina": disciplina["nume"],
                "Ore curs": disciplina["ore_curs"],
                "Credite": disciplina["credite"],
                "Număr examene": numar_examene
            })

    return rezultat

def get_curriculum_student(user_id):
    student = supabase.table("studenti").select("id").eq("utilizator_id", user_id).execute().data

    if not student:
        return []

    student_id = student[0]["id"]

    discipline = supabase.table("discipline").select("id, nume, ore_curs, credite").execute().data or []
    examene = supabase.table("examene").select("id, disciplina_id").execute().data or []
    specializari_discipline = supabase.table("specializari_discipline").select("specializare_id, disciplina_id").execute().data or []
    fise_inscriere = supabase.table("fise_inscriere").select("student_id, specializare_id").execute().data or []

    examene_dict = {}
    for e in examene:
        did = e["disciplina_id"]
        examene_dict[did] = examene_dict.get(did, 0) + 1

    specializare_student = None
    for f in fise_inscriere:
        if f["student_id"] == student_id:
            specializare_student = f["specializare_id"]
            break

    if specializare_student is None:
        return []

    rezultat = []

    for sd in specializari_discipline:
        if sd["specializare_id"] != specializare_student:
            continue

        disciplina = None
        for d in discipline:
            if d["id"] == sd["disciplina_id"]:
                disciplina = d
                break

        if not disciplina:
            continue

        rezultat.append({
            "Disciplina": disciplina["nume"],
            "Ore curs": disciplina["ore_curs"],
            "Credite": disciplina["credite"],
            "Număr examene": examene_dict.get(disciplina["id"], 0)
        })

    return rezultat
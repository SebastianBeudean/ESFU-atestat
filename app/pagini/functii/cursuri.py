from database.connection import supabase

def nume_specializari():
    rezultat = (
        supabase.table("specializari").select("nume").execute()
    )
    specializare = []
    for element in rezultat.data:
        specializare.append(element["nume"])

    return specializare

def nume_discipline():
    discipline_query = (
        supabase.table("discipline")
        .select("nume")
        .execute()
    )
    discipline_nume = []
    for element in discipline_query.data:
        discipline_nume.append(element["nume"])

    return discipline_nume

def discipline_specializare(nume_specializare):

    if nume_specializare == "Toate":
        return []
    else:
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


import db.neo4j_client as neo4j
from db.querys import Area_Query, Discipline_Query, Field_Query
import pandas as pd

import asyncio


def get_dash():
    db = neo4j.Neo4jClient()
    custom = asyncio.run(db.get_dashboard())

    return custom


def count_investigation_by_searcher(ids):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    db = neo4j.Neo4jClient()
    data = loop.run_until_complete(db.get_investigation_data(ids))
    loop.close()
    df = pd.DataFrame(data)
    return df


def covert_to_df():
    custom = get_dash()
    df = pd.DataFrame(custom)
    if df.empty:
        df = pd.DataFrame(
            columns=[
                "Organization",
                "Long",
                "Lat",
                "OrganizationType",
                "Researcher",
                "Surname",
                "Id",
                "Knowledge",
                "KnowledgeType",
                "City",
            ]
        )
    else:
        df.columns = [
            "Organization",
            "Long",
            "Lat",
            "OrganizationType",
            "Researcher",
            "Surname",
            "Id",
            "Knowledge",
            "KnowledgeType",
            "City",
        ]

    df["KnowledgeDiscipline"] = False
    df["KnowledgeArea"] = False
    df["KnowledgeSubdiscipline"] = False
    df["KnowledgeField"] = False

    def set_organization(row):
        for val in row["OrganizationType"]:
            if val == "Organization":
                row["OrganizationType"] = "Organización"
        return row

    def set_values(row):
        row["KnowledgeType"] = (
            row["KnowledgeType"][0] if row["KnowledgeType"] is not None else "Default"
        )
        if row["KnowledgeType"] in [
            "KnowledgeDiscipline",
            "KnowledgeArea",
            "KnowledgeSubdiscipline",
            "KnowledgeField",
        ]:
            row["KnowledgeType"] = {
                "KnowledgeDiscipline": "Disciplina",
                "KnowledgeArea": "Area",
                "KnowledgeSubdiscipline": "Subdisciplina",
                "KnowledgeField": "Campo",
            }[row["KnowledgeType"]]
            row[row["KnowledgeType"]] = True
        elif row["KnowledgeType"] == "t":
            row["KnowledgeType"] = "Default"
        return row

    df = df.apply(set_values, axis=1)
    df = df.apply(set_organization, axis=1)
    df.drop(
        columns=[
            "KnowledgeArea",
            "KnowledgeDiscipline",
            "KnowledgeSubdiscipline",
            "KnowledgeField",
        ],
        inplace=True,
    )

    return df


def get_knowledge_area_data(learning_type, df):
    df_filtered = df[df["KnowledgeType"] == learning_type]
    return df_filtered.groupby("Knowledge")["Researcher"].count()


def get_options(knowledge_list):
    options = [{"label": item, "value": item} for item in knowledge_list.keys()]
    options.append({"label": "Todas", "value": "Todas"})
    return options


def get_researchers_db():
    db = neo4j.Neo4jClient()
    custom = asyncio.run(db.get_researchers())
    df = pd.DataFrame(custom)
    if df.empty:
        df = pd.DataFrame(
            columns=[
                "CVU",
                "Nombre",
                "Apellido",
                "SNI",
                "Id",
                "País",
                "Estado",
                "Ciudad",
                "Lat",
                "Long",
                "Área",
                "Campos",
                "Disciplinas",
                "Institución",
            ]
        )
        df["CVU"] = "1239717"
        df["Nombre"] = "Alejandro"
        df["Apellido"] = "Medina Reyes"
        df["País"] = "México"
        df["Estado"] = "Chihuahua"
        df["Ciudad"] = "Juárez"
    else:
        df.columns = [
            "CVU",
            "Nombre",
            "Apellido",
            "SNI",
            "Id",
            "País",
            "Estado",
            "Ciudad",
            "Lat",
            "Long",
            "Área",
            "Campos",
            "Disciplinas",
            "Institución",
        ]
    df["Área"] = df["Área"].apply(lambda x: ", ".join(x))
    df["Campos"] = df["Campos"].apply(lambda x: ", ".join(x))
    df["Disciplinas"] = df["Disciplinas"].apply(lambda x: ", ".join(x))
    df["Institución"] = df["Institución"].apply(lambda x: ", ".join(x))
    return df


def get_papers_db():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    db = neo4j.Neo4jClient()
    data = loop.run_until_complete(db.get_papers())
    loop.close()
    df = pd.DataFrame(data)
    if df.empty:
        df = pd.DataFrame(
            columns=[
                "Nombre",
                "Tipo",
                "Id",
                "Area",
                "Campo",
                "Disciplina",
                "Institución",
                "Autor",
            ]
        )
        return df
    df.columns = ["Nombre", "Tipo", "Id", "Area", "Campo", "Disciplina"]
    return df


def get_institutions_db():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    db = neo4j.Neo4jClient()
    data = loop.run_until_complete(db.get_institutions())
    loop.close()
    df = pd.DataFrame(data)
    if df.empty:
        df = pd.DataFrame(
            columns=[
                "Nombre",
                "Tipo",
                "Pais",
                "Estado",
                "Ciudad",
                "Puntos",
                "Registrados",
            ]
        )
        df["Lat"] = "31.72955655"
        df["Long"] = "-106.39595258178568"
        df["Registrados"] = 0
        df["Pais"] = "México"
        df["Estado"] = "Chihuahua"
        df["Ciudad"] = "Juárez"
        df["Tipo"] = "Institución"
        return df
    df.columns = ["Nombre", "Tipo", "Pais", "Estado", "Ciudad", "Puntos", "Registrados"]
    df[["Lat", "Long"]] = df["Puntos"].str.split(",", expand=True)
    df["Lat"] = pd.to_numeric(df["Lat"])
    df["Long"] = pd.to_numeric(df["Long"])
    df = df.drop("Puntos", axis=1)
    return df


def get_area_db():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    db = neo4j.Neo4jClient()

    data = loop.run_until_complete(db.get_custom_query(query=Area_Query()))
    loop.close()
    df = pd.DataFrame(data)
    df.columns = ["Nombre", "Area"]

    return df


def get_field_db():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    db = neo4j.Neo4jClient()

    data = loop.run_until_complete(db.get_custom_query(query=Field_Query()))
    loop.close()
    df = pd.DataFrame(data)
    df.columns = ["Nombre", "Id", "Area"]

    return df


def get_discipline_db():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    db = neo4j.Neo4jClient()

    data = loop.run_until_complete(db.get_custom_query(query=Discipline_Query()))
    loop.close()
    df = pd.DataFrame(data)
    df.columns = ["Nombre", "Id", "Campo", "Area"]

    return df


def get_translate():
    return {
        "es": {
            "Download Table": "Descargar tabla",
            "Researchers": "Investigadores",
            "Scientific Paper": "Artículo científico",
            "Research Project": "Proyecto de investigación",
            "Research Group": "Grupo de investigación",
            "Patent": "Patente",
            "Publications": "Publicaciones",
            "Type": "Tipo",
            "Quantity": "Cantidad",
            "Total number of researchers": "Total de investigadores",
        },
        "en": {
            "Descargar tabla": "Download Table",
            "Investigadores": "Researchers",
            "Artículo científico": "Scientific Paper",
            "Proyecto de investigación": "Research Project",
            "Grupo de investigación": "Research Group",
            "Patente": "Patent",
            "Publicaciones": "Publications",
            "Tipo": "Type",
            "Cantidad": "Quantity",
            "Total de investigadores": "Total number of researchers",
        },
    }


def translate(text, lang):
    return get_translate()[lang].get(text, text)

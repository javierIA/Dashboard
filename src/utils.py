import db.neo4j_client as neo4j
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
    df.columns = ["Organization", "Long", "Lat", "OrganizationType",
                  "Researcher", "Surname", "Id", "Knowledge", "KnowledgeType", "City"]

    df["KnowledgeDiscipline"] = False
    df["KnowledgeArea"] = False
    df["KnowledgeSubdiscipline"] = False
    df["KnowledgeField"] = False

    def set_organization(row):
        for val in row['OrganizationType']:
            if val == "Organization":
                row["OrganizationType"] = "Organización"
        return row

    def set_values(row):

        row["KnowledgeType"] = row["KnowledgeType"][0] if row["KnowledgeType"] is not None else "Default"
        if row["KnowledgeType"] in ["KnowledgeDiscipline", "KnowledgeArea", "KnowledgeSubdiscipline", "KnowledgeField"]:
            row["KnowledgeType"] = {"KnowledgeDiscipline": "Disciplina", "KnowledgeArea": "Area",
                                    "KnowledgeSubdiscipline": "Subdisciplina", "KnowledgeField": "Campo"}[row["KnowledgeType"]]
            row[row["KnowledgeType"]] = True
        elif row["KnowledgeType"] == "t":
            row["KnowledgeType"] = "Default"
        return row

    df = df.apply(set_values, axis=1)
    df = df.apply(set_organization, axis=1)
    df.drop(columns=["KnowledgeArea", "KnowledgeDiscipline",
            "KnowledgeSubdiscipline", "KnowledgeField"], inplace=True)

    return df


def get_knowledge_area_data(learning_type, df):

    df_filtered = df[df["KnowledgeType"] == learning_type]
    return df_filtered.groupby("Knowledge")["Researcher"].count()


def get_options(knowledge_list):
    options = [{"label": item, "value": item}
               for item in knowledge_list.keys()]
    options.append({"label": "Todas", "value": "Todas"})
    return options

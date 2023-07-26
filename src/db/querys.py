def Area_Query():
    # convert to string
    qry = """
       MATCH (area:KnowledgeArea)
        RETURN 
 area.description as name,
 area.identifier as identifier
    """
    return qry


def Field_Query():
    return """
    MATCH (field:KnowledgeField)-[]->(area:KnowledgeArea)
    RETURN 
    field.description as name,
    field.identifier as identifier,
    area.identifier as area_identifier
    ORDER BY field.description

    """


def Discipline_Query():
    return """
    MATCH (discipline:KnowledgeDiscipline)-[]->(field:KnowledgeField)-[]->(area:KnowledgeArea)
    RETURN 
    discipline.description as name,
    discipline.identifier as identifier,
    field.identifier as field_identifier,
    area.identifier as area_identifier
    ORDER BY discipline.description
    """

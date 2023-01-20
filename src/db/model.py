import pandas as pd


def serializer_location(location):
    return {
        "identifier": location["identifier"],
        "website_url": location["website_url"],
        "external_number": location["external_number"],
        "street": location["street"],
        "name": location["name"],
        "foundation_year": location["foundation_year"],
        "location_point": location["location_point"],
        "x": location["location_point"].x,
        "y": location["location_point"].y,
        "neighborhood": location["neighborhood"],
        "postal_code": location["postal_code"]
    }


def seriaizer_organitation(organization):

    return {
        "external_number": organization["external_number"],
        "foundation_year": organization["foundation_year"],
        "identifier": organization["identifier"],
        "location_point": organization["location_point"],
        "name": organization["name"],
        "neighborhood": organization["neighborhood"],
        "postal_code": organization["postal_code"],
        "street": organization["street"],
        "website_url": organization["website_url"]
    }


def serializer_researcher(researcher):
    return {
        "id": researcher["id"],
        "birthdate": researcher["birthdate"],
        "created_at":	researcher["created_at"],
        "curp":	researcher["curp"],
        "cvu": researcher["cvu"],
        "email": researcher["email"],
        "first_surname": researcher["first_surname"],
        "gender":   researcher["gender"],
        "identifier":	researcher["identifier"],
        "interest_area": researcher["interest_area"],
        "main_contact_email": researcher["main_contact_email"],
        "name": researcher["name"],
        "rfc": researcher["rfc"],
        "second_surname": researcher["second_surname"],
        "show_info": researcher["show_info"],
        "sni_level": researcher["sni_level"],
        "user_id": researcher["user_id"],
        "validated": researcher["validated"]
    }


def serializer_knowledgediscipline(knowledge):
    return {
        "id": knowledge["id"],
        "cve": knowledge["cve"],
        "description": knowledge["description"],
        "identifier": knowledge["identifier"],
    }


def serializer_dashboard(dashboard):
    return {
        "Organization": dashboard["Organization"],
        "Location_point": dashboard["Location_point"],
        "OrganizationType": dashboard["OrganizationType"],
        "Researcher": dashboard["Researcher"],
        "Surname": dashboard["Surname"],
        "Knowledge=": dashboard["Knowledge"],
        "KnowledgeType": dashboard["KnowledgeType"]
    }

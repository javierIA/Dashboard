import dash_bootstrap_components as dbc
from dash import Input, Output, html, dcc
import pandas as pd


def generate_options(items, pathname):
    items = [i for i in set(items) if i is not None and pd.notna(i)]
    items.sort()
    if pathname == "/en":
        items.insert(0, "All")
    else:
        items.insert(0, "Todas")
    return [{"label": i, "value": i} for i in items]


def get_filterAreas(Area, pathname):
    areas = [
        {"label": row["Nombre"], "value": row["Area"]} for index, row in Area.iterrows()
    ]
    if pathname == "/en":
        areas.insert(0, {"label": "All", "value": "All"})
    else:
        areas.insert(0, {"label": "Todas", "value": "Todas"})
    return areas


def get_filters(institutions, pathname="/es"):
    city = institutions["Ciudad"].unique()
    city = generate_options(city, pathname)
    institution = institutions["Nombre"].unique()
    institution = generate_options(institution, pathname)
    if pathname == "/en":
        label_city = "City"
        placeholder_city = "Select a city"
        label_institution = "Institution"
        placeholder_institution = "Select an institution"
        value = "All"
    else:
        label_city = "Ciudad"
        placeholder_city = "Selecciona una ciudad"
        label_institution = "Institución"
        placeholder_institution = "Selecciona una institución"
        value = "Todas"
    return dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Label(label_city, style={"font-weight": "bold"}),
                    dcc.Dropdown(
                        id="city",
                        options=city,
                        value=value,
                        placeholder=placeholder_city,
                        className="dropdown",
                        style={
                            "width": "100%",
                            "font-size": "16px",
                            "height": "38px",
                            "padding": "6px 12px",
                            "border": "1px solid #ddd",
                            "border-radius": "4px",
                            "box-shadow": "inset 0px 1px 1px rgba(0, 0, 0, 0.075)",
                            "transition": "border-color ease-in-out 0.15s, box-shadow ease-in-out 0.15s",
                        },
                    ),
                ],
                width={"size": 6},
                xs={"size": 12},
                sm={"size": 12},
                md={"size": 6},
                lg={"size": 6},
                xl={"size": 6},
            ),
            dbc.Col(
                [
                    dbc.Label(label_institution, style={"font-weight": "bold"}),
                    dcc.Dropdown(
                        id="institution",
                        options=institution,
                        value=value,
                        placeholder=placeholder_institution,
                        className="dropdown",
                        style={
                            "width": "100%",
                            "font-size": "16px",
                            "height": "38px",
                            "padding": "6px 12px",
                            "border": "1px solid #ddd",
                            "border-radius": "4px",
                            "box-shadow": "inset 0px 1px 1px rgba(0, 0, 0, 0.075)",
                            "transition": "border-color ease-in-out 0.15s, box-shadow ease-in-out 0.15s",
                        },
                    ),
                ],
                width={"size": 6},
                xs={"size": 12},
                sm={"size": 12},
                md={"size": 6},
                lg={"size": 6},
                xl={"size": 6},
            ),
        ]
    )


def get_knowledge_filter(areas, pathname="/es"):
    areas = get_filterAreas(areas, pathname)

    if pathname == "/en":
        label_area = "Knowledge Area"
        placeholder_area = "Select an area"
        label_field = "Field"
        placeholder_field = "Select a field"
        label_discipline = "Discipline"
        placeholder_discipline = "Select a discipline"
    else:
        label_area = "Área de conocimiento"
        placeholder_area = "Selecciona un área"
        label_field = "Campo"
        placeholder_field = "Selecciona un campo"
        label_discipline = "Disciplina"
        placeholder_discipline = "Selecciona una disciplina"

    return dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Label(label_area, style={"font-weight": "bold"}),
                    dcc.Dropdown(
                        id="area",
                        options=areas,
                        value="All",
                        placeholder=placeholder_area,
                        className="dropdown",
                        multi=True,
                        style={
                            "width": "100%",
                            "font-size": "16px",
                            "height": "38px",
                            "padding": "6px 12px",
                            "border": "1px solid #ddd",
                            "border-radius": "4px",
                            "box-shadow": "inset 0px 1px 1px rgba(0, 0, 0, 0.075)",
                            "transition": "border-color ease-in-out 0.15s, box-shadow ease-in-out 0.15s",
                        },
                    ),
                ],
            ),
            dbc.Col(
                [
                    dbc.Label(label_field, style={"font-weight": "bold"}),
                    dcc.Dropdown(
                        id="field",
                        options=[{"label": "All", "value": "All"}],
                        value="All",
                        placeholder=placeholder_field,
                        className="dropdown",
                        search_value="",
                        multi=True,
                        style={
                            "width": "100%",
                            "font-size": "16px",
                            "height": "38px",
                            "padding": "6px 12px",
                            "border": "1px solid #ddd",
                            "border-radius": "4px",
                            "box-shadow": "inset 0px 1px 1px rgba(0, 0, 0, 0.075)",
                            "transition": "border-color ease-in-out 0.15s, box-shadow ease-in-out 0.15s",
                        },
                    ),
                ],
            ),
            dbc.Col(
                [
                    dbc.Label(label_discipline, style={"font-weight": "bold"}),
                    dcc.Dropdown(
                        id="discipline",
                        options=[{"label": "All", "value": "All"}],
                        value="All",
                        placeholder=placeholder_discipline,
                        className="dropdown",
                        multi=True,
                        style={
                            "width": "100%",
                            "font-size": "16px",
                            "height": "38px",
                            "padding": "6px 12px",
                            "border": "1px solid #ddd",
                            "border-radius": "4px",
                            "box-shadow": "inset 0px 1px 1px rgba(0, 0, 0, 0.075)",
                            "transition": "border-color ease-in-out 0.15s, box-shadow ease-in-out 0.15s",
                        },
                    ),
                ],
                width={"size": 4},
                xs={"size": 12},
                sm={"size": 12},
                md={"size": 4},
                lg={"size": 4},
                xl={"size": 4},
            ),
            html.Br(),
            html.Br(),
            html.Br(),
        ]
    )

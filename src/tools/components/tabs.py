import dash_bootstrap_components as dbc
from dash import Input, Output, html, dcc
import pandas as pd


def generate_options(items):
    items = [i for i in set(items) if i is not None and pd.notna(i)]
    items.sort()
    items.insert(0, "Todas")

    return [{"label": i, "value": i} for i in items]


def get_filterAreas(Area):
    areas = [
        {"label": row["Nombre"], "value": row["Area"]} for index, row in Area.iterrows()
    ]
    areas.insert(0, {"label": "Todas", "value": "Todas"})
    return areas


def get_filters(institutions):
    city = institutions["Ciudad"].unique()
    city = generate_options(city)
    institution = institutions["Nombre"].unique()
    institution = generate_options(institution)

    return dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Label("Ciudad", style={"font-weight": "bold"}),
                    dcc.Dropdown(
                        id="city",
                        options=city,
                        value="Todas",
                        placeholder="Selecciona una ciudad",
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
                    dbc.Label("Institución", style={"font-weight": "bold"}),
                    dcc.Dropdown(
                        id="institution",
                        options=institution,
                        value="Todas",
                        placeholder="Selecciona una institución",
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


def get_knowledge_filter(areas):
    areas = get_filterAreas(areas)

    return dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Label("Área de conocimiento", style={"font-weight": "bold"}),
                    dcc.Dropdown(
                        id="area",
                        options=areas,
                        value="Todas",
                        placeholder="Selecciona un área",
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
                    dbc.Label("Campo", style={"font-weight": "bold"}),
                    dcc.Dropdown(
                        id="field",
                        options=[{"label": "Todas", "value": "Todas"}],
                        value="Todas",
                        placeholder="Selecciona un campo",
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
                    dbc.Label("Disciplina", style={"font-weight": "bold"}),
                    dcc.Dropdown(
                        id="discipline",
                        options=[{"label": "Todas", "value": "Todas"}],
                        value="Todas",
                        placeholder="Selecciona una disciplina",
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

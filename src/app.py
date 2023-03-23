import base64
import dash
from dash.dependencies import Input, Output, State
from dash import html
from dash import dcc
import pandas as pd
import plotly.graph_objects as go
from tools.components.maps import get_map
from tools.components.table import get_table
from tools.components.graph import get_graph, get_graph_groupBy, transform_data
from tools.components.tabs import get_filters, get_knowledge_filter
from utils import (
    get_researchers_db,
    get_papers_db,
    get_institutions_db,
    get_area_db,
    get_field_db,
    get_discipline_db,
)
import urllib
import dash_bootstrap_components as dbc
import asyncio
import colorlover as cl

external_stylesheets = [
    dbc.themes.COSMO,
]
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=external_stylesheets,
)
app.title = "I2C Dashboard"
app.config.suppress_callback_exceptions = True

# Get the data
researchers = get_researchers_db()
institutions = get_institutions_db()
papers = get_papers_db()
areas = get_area_db()


server = app.server
app.layout = dbc.Container(
    fluid=True,
    style={"backgroundColor": "#f5f7ff"},
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        get_filters(institutions),
                        html.Br(),
                        get_knowledge_filter(areas),
                        html.Br(),
                    ],
                    lg=12,
                    md=12,
                    sm=12,
                ),
            ],
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        get_graph(papers),
                        html.Br(),
                    ],
                    lg=4,
                    md=6,
                    sm=12,
                ),
                dbc.Col(
                    children=[
                        dcc.Graph(
                            id="map-graph",
                            config=dict(displayModeBar=False, scrollZoom=True),
                            animate=True,
                            figure=get_map(researchers, institutions),
                            animation_options=dict(
                                frame=dict(duration=500, redraw=False),
                                transition=dict(duration=500),
                                easing="linear",
                                fromcurrent=True,
                                mode="immediate",
                            ),
                        ),
                        html.Div(
                            id="researcher-count",
                            className="display-6 text-center",
                            style={
                                "font-size": "2rem",
                                "font-weight": "bold",
                                "color": "#000000",
                                "font-family": "apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica Neue,Arial,Noto Sans,sans-serif,Apple Color Emoji,Segoe UI Emoji,Segoe UI Symbol,Noto Color Emoji",
                            },
                        ),
                    ],
                    lg=8,
                    md=6,
                    sm=12,
                ),
            ],
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        dbc.Label("Investigadores"),
                        get_table(researchers),
                        html.Br(),
                        dbc.Button(
                            "Descargar tabla",
                            id="btn_xlsx",
                            className="btn btn-primary btn-lg",
                        ),
                        dcc.Download(id="download-dataframe-xlsx"),
                    ],
                    lg=9,
                    md=6,
                    sm=12,
                ),
                dbc.Col(
                    children=[
                        html.Br(),
                        get_graph_groupBy(researchers),
                    ],
                    lg=3,
                    md=6,
                    sm=12,
                ),
            ],
        ),
    ],
)


# Define the callback function
@app.callback(
    Output("download-dataframe-xlsx", "data"),
    Input("btn_xlsx", "n_clicks"),
    State("researcher-table", "data"),
    prevent_initial_call=True,
)
def func(n_clicks, data):
    data = pd.DataFrame(data)
    return dcc.send_data_frame(data.to_excel, "Dash.xlsx")


@app.callback(
    Output("map-graph", "figure"),
    Input("institution", "value"),
    prevent_initial_call=True,
)
def update_map(institution):
    if institution is None or institution == "Todas":
        mapUpdate = get_map(researchers, institutions)
        zoom = 5
    else:
        Lat = institutions[institutions["Nombre"] == institution]["Lat"].values[0]
        Long = institutions[institutions["Nombre"] == institution]["Long"].values[0]
        zoom = 10
        mapUpdate = get_map(researchers, institutions)
        mapUpdate.update_layout(
            mapbox_center={"lat": Lat, "lon": Long},
            mapbox_zoom=zoom,
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            uirevision=True,  # Agregar esta línea
        )
        mapUpdate.update(layout=dict(uirevision=True))
    return mapUpdate


@app.callback(
    Output("field", "options"),
    Input("area", "value"),
    prevent_initial_call=True,
)
def update_field(areas):
    if areas is None or areas == "Todas":
        return []
    else:
        fields = get_field_db()
        fields_df = pd.DataFrame(fields)
        for area in areas:
            filtered_fields = fields_df.loc[fields_df["Area"] == area]
            options = filtered_fields[["Nombre", "Id"]].to_dict("records")

        return [
            {"label": option["Nombre"], "value": option["Id"]} for option in options
        ]


@app.callback(Output("discipline", "options"), Input("field", "value"))
def update_discipline(fields):
    if fields is None or fields == "Todas":
        return []
    else:
        for field in fields:
            disciplines = get_discipline_db()
            disciplines_df = pd.DataFrame(disciplines)
            filtered_disciplines = disciplines_df.loc[disciplines_df["Campo"] == field]
            options = filtered_disciplines[["Nombre", "Id"]].to_dict("records")
            return [
                {"label": option["Nombre"], "value": option["Id"]} for option in options
            ]


@app.callback(
    Output("researcher-table", "data"),
    Input("area", "value"),
    Input("area", "options"),
    Input("field", "value"),
    Input("field", "options"),
    Input("discipline", "value"),
    Input("discipline", "options"),
    Input("institution", "value"),
    Input("city", "value"),
    prevent_initial_call=True,
)
def update_table(
    area,
    area_label,
    field,
    field_label,
    discipline,
    discipline_label,
    institution,
    city,
):
    area = [] if area is None or area == "Todas" else area
    field = [] if field is None or "Todas" in field else field
    discipline = [] if discipline is None or "Todas" in discipline else discipline
    institution = "" if institution is None or institution == "Todas" else institution
    city = "" if city is None or city == "Todas" else city
    selected_areas = [
        option["label"] for option in area_label if option["value"] in area
    ]
    selected_fields = [
        option["label"] for option in field_label if option["value"] in field
    ]
    selected_disciplines = [
        option["label"] for option in discipline_label if option["value"] in discipline
    ]

    # Filter the data
    filtered_researchers = researchers
    if len(area) > 0:
        filtered_researchers = filtered_researchers[
            filtered_researchers["Área"].isin(selected_areas)
        ]
    if len(field) > 0:
        filtered_researchers = filtered_researchers[
            filtered_researchers["Campos"].isin(selected_fields)
        ]
    if len(discipline) > 0:
        filtered_researchers = filtered_researchers[
            filtered_researchers["Disciplinas"].isin(selected_disciplines)
        ]
    if institution != "":
        filtered_researchers = filtered_researchers[
            filtered_researchers["Institución"] == institution
        ]
    if city != "":
        filtered_researchers = filtered_researchers[
            filtered_researchers["Ciudad"] == city
        ]

    # Return the filtered data in the expected format
    return filtered_researchers.to_dict("records")


@app.callback(
    Output("researcher-count", "children"),
    Input("area", "value"),
    Input("area", "options"),
    Input("field", "value"),
    Input("field", "options"),
    Input("discipline", "value"),
    Input("discipline", "options"),
    Input("institution", "value"),
    Input("city", "value"),
    prevent_initial_call=True,
)
def update_count(
    area,
    area_label,
    field,
    field_label,
    discipline,
    discipline_label,
    institution,
    city,
):
    area = [] if area is None or area == "Todas" else area
    field = [] if field is None or "Todas" in field else field
    discipline = [] if discipline is None or "Todas" in discipline else discipline
    institution = "" if institution is None or institution == "Todas" else institution
    selected_areas = [
        option["label"] for option in area_label if option["value"] in area
    ]
    selected_fields = [
        option["label"] for option in field_label if option["value"] in field
    ]
    selected_disciplines = [
        option["label"] for option in discipline_label if option["value"] in discipline
    ]
    city = "" if city is None or city == "Todas" else city
    # Filter the data
    filtered_researchers = researchers
    if len(area) > 0:
        filtered_researchers = filtered_researchers[
            filtered_researchers["Área"].isin(selected_areas)
        ]
    if len(field) > 0:
        filtered_researchers = filtered_researchers[
            filtered_researchers["Campos"].isin(selected_fields)
        ]
    if len(discipline) > 0:
        filtered_researchers = filtered_researchers[
            filtered_researchers["Disciplinas"].isin(selected_disciplines)
        ]
    if institution != "":
        filtered_researchers = filtered_researchers[
            filtered_researchers["Institución"] == institution
        ]
    if city != "":
        filtered_researchers = filtered_researchers[
            filtered_researchers["Ciudad"] == city
        ]

    # Return the filtered data in the expected format
    return "Total de investigadores: " + str(len(filtered_researchers))


@app.callback(
    Output("graph_papers", "figure"),
    Input("area", "value"),
    Input("field", "value"),
    Input("discipline", "value"),
)
def update_graph_papers(area, field, discipline):
    area = [] if area is None or area == "Todas" else area
    field = [] if field is None or "Todas" in field else field
    discipline = [] if discipline is None or "Todas" in discipline else discipline
    # Filter the data
    papers = get_papers_db()
    papers_df = pd.DataFrame(papers)
    if len(area) > 0:
        papers_df = papers_df[papers_df["Area"].isin(area)]
    if len(field) > 0:
        papers_df = papers_df[papers_df["Campo"].isin(field)]
    if len(discipline) > 0:
        papers_df = papers_df[papers_df["Disciplina"].isin(discipline)]
    type_count_map = {
        "ScientificPaper": 0,
        "ResearchProject": 1,
        "ResearchGroup": 2,
        "Patent": 3,
    }
    type_labels = (
        "Artículo científico",
        "Proyecto de investigación",
        "Grupo de investigación",
        "Patente",
    )
    counts = papers_df.groupby("Tipo").size().reindex(type_count_map.keys()).tolist()
    colors = cl.scales["9"]["qual"]["Paired"]
    colors = cl.interp(colors, len(type_labels))

    bar_data = [go.Bar(x=type_labels, y=counts, marker=dict(color=colors))]
    layout = go.Layout(
        xaxis=dict(title="Tipo"),
        yaxis=dict(title="Cantidad"),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(color="black"),
    )
    return go.Figure(data=bar_data, layout=layout)


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8020, debug=True)

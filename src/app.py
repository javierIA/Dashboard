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
    translate,
    
)
import dash_bootstrap_components as dbc
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

language = "es"
#   Get the data
researchers = get_researchers_db()
institutions = get_institutions_db()
papers = get_papers_db()
areas = get_area_db()
mapChihuahua = get_map(researchers, institutions)


server = app.server
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    dcc.Store(id='language-store')  # Almacena el idioma seleccionado
])
# Agrega el componente de almacenamiento a tu layout


# Modifica tu callback para usar el estado del componente de almacenamiento
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')],
              [State('language-store', 'data')])  # Recupera el idioma seleccionado
def display_page(pathname, language):
    if not language:
        language = 'es'
    
    if pathname == '/':
        return  dbc.Container(
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
                            figure=mapChihuahua,
                            config={"displayModeBar": False, "scrollZoom": True},
                            responsive=True,
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
    elif pathname == '/en':
        return dbc.Container(
    fluid=True,
    style={"backgroundColor": "#f5f7ff"},
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        get_filters(institutions,pathname='/en'),
                        html.Br(),
                        get_knowledge_filter(areas,pathname='/en'),
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
                        get_graph(papers,pathname='/en'),
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
                            figure=mapChihuahua,
                            config={"displayModeBar": False, "scrollZoom": True},
                            responsive=True,
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
                        dbc.Label("Researchers"),
                        get_table(df=researchers,pathname="/en"),
                        html.Br(),
                        dbc.Button(
                            "Download Table",
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
                        get_graph_groupBy(data=researchers,pathname="/en"),
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
    [
        Output("map-graph", "figure"),
        Output("map-graph", "config"),
    ],
    [
        Input("institution", "value"),
        Input('url', 'pathname')
    ],
    prevent_initial_call=True,
)
def update_map(institution, pathname):
    if pathname == "/en":
        if institution is None or institution == "All":
            mapUpdate = get_map(researchers, institutions)
        else:
            Lat = institutions[institutions["Name"] == institution]["Lat"].values[0]
            Long = institutions[institutions["Name"] == institution]["Long"].values[0]
            print(Lat, Long)
            zoom = 8
            mapUpdate = get_map(
                researchers=researchers,
                institutions=institutions,
                center={"lat": Lat, "lon": Long},
                zoom=zoom,
            ).update_layout(
                mapbox_zoom=zoom,
                mapbox_center={"lat": Lat, "lon": Long},
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
            )
            return mapUpdate, map_config
    else:
        if institution is None or institution == "Todas" or institution == "All":
            mapUpdate = get_map(researchers, institutions)
        else:
            Lat = institutions[institutions["Nombre"] == institution]["Lat"].values[0]
            Long = institutions[institutions["Nombre"] == institution]["Long"].values[0]
            print(Lat, Long)
            zoom = 8
            mapUpdate = get_map(
                researchers=researchers,
                institutions=institutions,
                center={"lat": Lat, "lon": Long},
                zoom=zoom,
            ).update_layout(
                mapbox_zoom=zoom,
                mapbox_center={"lat": Lat, "lon": Long},
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
            )
        map_config = dict(scrollZoom=True)
        return mapUpdate, map_config

@app.callback(
    Output("field", "options"),
    Input("area", "value"),
    prevent_initial_call=True,
)
def update_field(areas):
    if areas is None or areas == "Todas" or areas == "All":
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
    if fields is None or fields == "Todas" or fields == "All":
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
    area = [] if area is None or area == "Todas" or area == "All" else area
    field = [] if field is None or ("Todas" in field or "All" in field) else field
    discipline = [] if discipline is None or ("Todas" in discipline or "All" in discipline) else discipline
    institution = "" if institution is None or (institution == "Todas" or institution == "All") else institution
    city = "" if city is None or (city == "Todas" or city == "All") else city

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
    [
        Input("area", "value"),
        Input("area", "options"),
        Input("field", "value"),
        Input("field", "options"),
        Input("discipline", "value"),
        Input("discipline", "options"),
        Input("institution", "value"),
        Input("city", "value"),
        Input("url", "pathname"),
    ],
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
    pathname,
):
    area = [] if area is None or ("Todas" in area or "All" in area) else area
    field = [] if field is None or ("Todas" in field or "All" in field) else field
    discipline = [] if discipline is None or ("Todas" in discipline or "All" in discipline) else discipline
    institution = "" if institution is None or (institution == "Todas" or institution == "All") else institution

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

    if pathname == "/en":
        return translate("Total number of researchers", "en") + ": " + str(len(filtered_researchers))
    else:
        return translate("Total de investigadores", "es") + ": " + str(len(filtered_researchers))



@app.callback(
    Output("graph_papers", "figure"),
    Input("area", "value"),
    Input("field", "value"),
    Input("discipline", "value"),
    Input("url", "pathname"),
)
def update_graph_papers(area, field, discipline,pathname):
    area = [] if area is None or area == "Todas" or "All" else area
    field = [] if field is None or "Todas" or "All" in field else field
    discipline = [] if discipline is None or "Todas" or "All" in discipline else discipline

    # # Filter the data
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

    if pathname == "/en":
        type_labels = (
            "Scientific Paper",
            "Research Project",
            "Research Group",
            "Patent",
        )

        bar_data = [go.Bar(x=type_labels, y=counts, marker=dict(color=colors))]
        layout = go.Layout(
            title="Papers",
            xaxis=dict(title="Type"),
            yaxis=dict(title="Number of papers"),
            plot_bgcolor="rgba(0, 0, 0, 0)",
            paper_bgcolor="rgba(0, 0, 0, 0)",
            font=dict(color="black", size=12),
            margin=dict(l=0, r=0, t=30, b=0),
        )
    else:
        bar_data = [go.Bar(x=type_labels, y=counts, marker=dict(color=colors))]
        layout = go.Layout(
            title="Publicaciones",
            xaxis=dict(title="Tipo"),
            yaxis=dict(title="Número de publicaciones"),
            plot_bgcolor="rgba(0, 0, 0, 0)",
            paper_bgcolor="rgba(0, 0, 0, 0)",
            font=dict(color="black", size=12),
            margin=dict(l=0, r=0, t=30, b=0),
        )
    return go.Figure(data=bar_data, layout=layout)


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8020)

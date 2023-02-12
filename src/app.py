import base64
import dash
from dash.dependencies import Input, Output, State
from dash import html
from dash import dcc
import pandas as pd
import plotly.graph_objects as go
from tools.components.maps import get_map
from utils import covert_to_df, get_knowledge_area_data, get_options, count_investigation_by_searcher
from dash import dash_table
import urllib
import dash_bootstrap_components as dbc
import asyncio
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, meta_tags=[
                {"name": "viewport", "content": "width=device-width, initial-scale=1"}], external_stylesheets=external_stylesheets)
app.title = 'I2E Dashboard'
app.config.suppress_callback_exceptions = True


def get_field_options(field_name):
    field_data = get_knowledge_area_data(field_name, raw)
    return get_options(field_data)


raw = covert_to_df()
server = app.server
mapa = get_map(raw)
datatemp = raw[["Researcher", "Surname", "Organization",
                "City", "Knowledge"]].drop_duplicates()
data_dict = datatemp.to_dict('records')

data_table = dash_table.DataTable(
    id='researcher-table',
    data=data_dict,
    page_size=10,
    page_action="native",
    columns=[{"name": "Nombre", "id": "Researcher"},
             {"name": "Apellido", "id": "Surname"},
             {"name": "Organización", "id": "Organization"},
             {"name": "Ciudad", "id": "City"},
             {"name": "Conocimiento", "id": "Knowledge"}],
    filter_action="native",
    sort_action="native",
    sort_mode="single",
    column_selectable="single",
    style_table={"fontFamily": '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji"'},
    style_header={'backgroundColor': 'white',
                  'fontWeight': 'bold', 'padding': '0.75rem'},
    style_cell={"fontFamily": '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji"',
                'fontWeight': '400', 'lineHeight': '1.5', 'color': '#212529', 'textAlign': 'left', 'whiteSpace': 'normal', 'height': 'auto', 'padding': '0.75rem', 'border': '1px solid #dee2e6', 'verticalAlign': 'top'}
)

area_options = get_field_options("Area")
discipline_options = get_field_options("Disciplina")
subdiscipline_options = get_field_options("Sub-disciplina")
field_options = get_field_options("Campo")
subfield_options = get_field_options("Sub-campo")

app.layout = html.Div(className="container-fluid ", children=[
    html.Div(className="", children=[
        html.Div(className="container-fluid", children=[
            html.Div(className="row", children=[
                dcc.Graph(
                    id="map-graph",
                    figure=mapa,
                    config=dict(displayModeBar=False, scrollZoom=True),
                    className="col-md-8 px-4",
                    animate=True,
                    animation_options=dict(
                        frame=dict(duration=500, redraw=False),
                        transition=dict(duration=500),
                        easing="linear",
                        fromcurrent=True,
                        mode="immediate",
                    ),

                ),

                dcc.Graph(
                    id="knowledge-area-bar-chart",
                    config=dict(displayModeBar=False, scrollZoom=True),
                    className="col-md-4 px-4",
                    animate=True,
                    animation_options=dict(
                        frame=dict(duration=500, redraw=False),
                        transition=dict(duration=500),
                        easing="linear",
                        fromcurrent=True,
                        mode="immediate",
                    ),
                )
            ]),
            html.Div(
                className="row", children=[
                    html.Div(
                        className="col-md-12 text-center", children=[
                            html.Div(
                                id='researcher-count', className="display-6 text-center", style={"font-size": "2rem", "font-weight": "bold", "color": "#000000", "font-family": "apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica Neue,Arial,Noto Sans,sans-serif,Apple Color Emoji,Segoe UI Emoji,Segoe UI Symbol,Noto Color Emoji"}),

                        ]
                    ),
                ]
            ),
            html.Div(className="row", children=[
                html.Div(className="col-md-4", children=[
                    html.Label("Organization", className="px-4", style={"font-size": "1.2rem", "color": "#000000",
                               "font-family": "apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica Neue,Arial,Noto Sans,sans-serif,Apple Color Emoji,Segoe UI Emoji,Segoe UI Symbol,Noto Color Emoji"}),
                    dcc.Dropdown(
                        id="Organization",
                        options=[{"label": Organization, "value": Organization} for Organization in raw["Organization"].unique(
                        ).tolist() + ["Todas"] if Organization != "Organization"],
                        value="Todas",
                        className="form-control px-4"
                    )
                ]),
                html.Div(className="col-md-4", children=[
                    html.Label("Ciudad", className="px-4", style={"font-size": "1.2rem", "color": "#000000",
                               "font-family": "apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica Neue,Arial,Noto Sans,sans-serif,Apple Color Emoji,Segoe UI Emoji,Segoe UI Symbol,Noto Color Emoji"}),
                    dcc.Dropdown(
                        id="city-dropdown",
                        options=[{"label": city, "value": city}
                                 for city in raw["City"].unique().tolist() + ["Todas"] if city != "City"],
                        value="Todas",
                        className="form-control px-4"
                    )
                ]),
                html.Div(className="col-md-4", children=[
                    html.Label("Tipo de aprendizaje", className="px-4", style={"font-size": "1.2rem", "color": "#000000",
                               'font-family': 'apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica Neue,Arial,Noto Sans,sans-serif,Apple Color Emoji,Segoe UI Emoji,Segoe UI Symbol,Noto Color Emoji'}),
                    dcc.Dropdown(
                        id="learning-type-dropdown",
                        options=[{"label": learning_type, "value": learning_type} for learning_type in raw["KnowledgeType"].unique(
                        ).tolist() + ["Todas"] if learning_type != "KnowledgeDiscipline"],
                        value="Todas",
                        className="form-control px-4"
                    )
                ]),

                html.Div(className="col-md-4", children=[
                    html.Label("Area de conocimiento", className="px-4", style={"font-size": "1.2rem", "color": "#000000",
                               'font-family': 'apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica Neue,Arial,Noto Sans,sans-serif,Apple Color Emoji,Segoe UI Emoji,Segoe UI Symbol,Noto Color Emoji'}),
                    dcc.Dropdown(
                        id="Area",
                        options=area_options,
                        value="Todas",
                        multi=True,
                        className="form-control px-4"
                    )
                ]),
                html.Div(className="col-md-4", children=[
                    html.Label("Disciplina", className="px-4", style={"font-size": "1.2rem", "color": "#000000",
                               'font-family': 'apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica Neue,Arial,Noto Sans,sans-serif,Apple Color Emoji,Segoe UI Emoji,Segoe UI Symbol,Noto Color Emoji'}),
                    dcc.Dropdown(
                        id="Discipline",
                        options=discipline_options,
                        value="Todas",
                        multi=True,
                        className="form-control px-4"
                    )
                ]),
                html.Div(className="col-md-4", children=[
                    html.Label("Campo", className="px-4", style={"font-size": "1.2rem", "color": "#000000", 'font-family': 'apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica Neue,Arial,Noto Sans,sans-serif,Apple Color Emoji,Segoe UI Emoji,Segoe UI Symbol,Noto Color Emoji'}),                    dcc.Dropdown(
                        id="Field",
                        multi=True,
                        options=field_options,
                        value="Todas",
                        className="form-control px-4"
                    )
                ]),
            ]),
            html.Div(className="row", children=[
                html.Div(className="col-md-6", children=[
                    data_table,
                    html.Br(),
                    html.Button("Descargar tabla", id="btn_xlsx",
                                className="btn btn-primary btn-lg"),
                    dcc.Download(id="download-dataframe-xlsx"),
                ]),
                html.Div(className="col-md-6", children=[
                    html.Label("Tipos de conocimiento"),
                    dcc.Graph(
                        id="knowledge-type-pie-chart",
                        config=dict(displayModeBar=False, scrollZoom=True),
                        className="col-md-12 px-4",
                        animate=True,
                        animation_options=dict(
                            frame=dict(duration=500, redraw=False),
                            transition=dict(duration=300),
                            easing="linear",
                            fromcurrent=True,
                            mode="immediate"
                        ),


                    )
                ]),
            ])

        ])
    ])
])

# Define the callback function


@app.call   back(
    Output(component_id='researcher-count', component_property='children'),
    [Input(component_id='Organization', component_property='value'),
     Input(component_id='learning-type-dropdown', component_property='value'),
     Input(component_id='city-dropdown', component_property='value'),
     Input(component_id='Area', component_property='value'),
     Input(component_id='Discipline', component_property='value'),
     Input(component_id='Field', component_property='value')
     ]
)
def update_researcher_count(selected_organization, learning_type, city, area, discipline, field):
    filtered_data = raw

    if selected_organization != 'Todas':
        filtered_data = filtered_data[filtered_data['Organization'].isin(
            [selected_organization])]

    if learning_type != 'Todas':
        filtered_data = filtered_data[filtered_data['KnowledgeType'].isin(
            [learning_type])]

    if city != 'Todas':
        filtered_data = filtered_data[filtered_data['City'].isin(
            [city])]

    if area and 'Todas' not in area:
        filtered_data = filtered_data[filtered_data['Area'].isin(area)]

    if discipline and 'Todas' not in discipline:
        filtered_data = filtered_data[filtered_data['Disciplina'].isin(
            discipline)]

    if field and 'Todas' not in field:
        filtered_data = filtered_data[filtered_data['Knowledge'].isin(field)]

    unique_researchers = filtered_data['Id'].unique()
    unique_researchers = pd.DataFrame(unique_researchers, columns=['Id'])

    count_researchers = len(unique_researchers)
    count_investigations = count_investigation_by_searcher(
        unique_researchers['Id'].unique())[0].sum()

    if count_researchers == 1:
        return f'{count_researchers} Investigador con {count_investigations} Investigación(es)'

    return f'{count_researchers} Investigadores con {count_investigations} Investigaciones'


@ app.callback(
    Output("knowledge-area-bar-chart", "figure"),
    [Input("learning-type-dropdown", "value"),
     Input("Organization", "value"),
     Input("city-dropdown", "value")])
def update_knowledge_area_bar_chart(learning_type, selected_organization, city):
    filtered_data = raw
    if selected_organization != 'Todas':
        filtered_data = filtered_data[filtered_data['Organization']
                                      == selected_organization]
    if learning_type != 'Todas':
        filtered_data = filtered_data[filtered_data['KnowledgeType']
                                      == learning_type]
    if city != 'Todas':
        filtered_data = filtered_data[filtered_data['City'] == city]

    count_df = filtered_data['Knowledge'].value_counts()
    return {
        "data": [go.Bar(x=count_df.index, y=count_df.values)],
        "layout": go.Layout(title="Áreas de Conocimiento", xaxis={"title": "Área de Conocimiento"}, yaxis={"title": "Número de Investigadores Únicos"}, template="seaborn")
    }


@ app.callback(
    dash.dependencies.Output("map-graph", "figure"),
    [dash.dependencies.Input("Organization", "value"), dash.dependencies.Input("city-dropdown", "value")])
def update_map_Org(Organization, City):
    filtered_data = raw
    if Organization != "Todas":
        filtered_data = filtered_data[filtered_data['Organization']
                                      == Organization]
    if City != "Todas":
        filtered_data = filtered_data[filtered_data['City'] == City]
    if City == "Todas" and Organization == "Todas":
        filtered_data = raw
        longitude = -106.088747
        latitude = 28.635308
        map_zoom = 6
    else:
        longitude = filtered_data['Long'].unique().mean()
        latitude = filtered_data['Lat'].unique().mean()
        map_zoom = 8

    map_filtered = get_map(filtered_data).update_layout(
        mapbox_zoom=map_zoom, mapbox_center={"lat": latitude, "lon": longitude})

    return map_filtered


@ app.callback(
    Output(component_id='researcher-table', component_property='data'),
    [Input(component_id='map-graph', component_property='selectedData'),
     Input(component_id='learning-type-dropdown',
           component_property='value'),
     Input(component_id='Organization', component_property='value'),
     Input(component_id='city-dropdown', component_property='value')]
)
def update_table(selected_data, learning_type, organization, city):
    raw.drop_duplicates(subset="Researcher", inplace=True)
    filtered_data = raw
    filtered_data = filtered_data[filtered_data["Researcher"] != ""]
    # eliminar la columna organizationtype
    filtered_data = filtered_data.drop(columns=['OrganizationType'])
    if selected_data is not None:
        selected_points = [point['customdata']
                           for point in selected_data['points']]
        filtered_data = filtered_data[filtered_data["Organization"].isin(
            selected_points)]
    if learning_type != "Todas":

        filtered_data = filtered_data[filtered_data["KnowledgeType"]
                                      == learning_type]
    if organization != "Todas":
        filtered_data = filtered_data[filtered_data["Organization"]
                                      == organization]
    if city != "Todas":
        filtered_data = filtered_data[filtered_data["City"] == city]

    return filtered_data.to_dict('records')


@ app.callback(
    Output("knowledge-type-pie-chart", "figure"),
    [Input("learning-type-dropdown", "value"),
     Input("Organization", "value"),
     Input("city-dropdown", "value"),
     ])
def update_knowledge_type_pie_chart(learning_type, organization, city):
    filtered_data = raw
    if learning_type != "Todas":
        filtered_data = filtered_data[filtered_data["KnowledgeType"]
                                      == learning_type]
    if organization != "Todas":
        filtered_data = filtered_data[filtered_data["Organization"]
                                      == organization]
    if city != "Todas":
        filtered_data = filtered_data[filtered_data["City"] == city]
    df = filtered_data.groupby("Knowledge")["Researcher"].count()
    return {
        "data": [go.Pie(labels=df.index, values=df.values)],
        "layout": go.Layout(title="Tipos de Conocimiento", template="seaborn")
    }


@ app.callback(
    Output("download-dataframe-xlsx", "data"),
    Input("btn_xlsx", "n_clicks"),
    State("researcher-table", "data"),
    prevent_initial_call=True,
)
def func(n_clicks, data):
    data = pd.DataFrame(data)

    return dcc.send_data_frame(data.to_excel, "Dash.xlsx")


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8020, debug=True)

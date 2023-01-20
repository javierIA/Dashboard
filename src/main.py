import base64
import dash
from dash.dependencies import Input, Output, State
from dash import html
from dash import dcc
import datetime as dt
import pandas as pd
import plotly.graph_objects as go
from tools.components.maps import get_map
from utils import covert_to_df, get_knowledge_area_data, get_options
from dash import dash_table
import urllib


def getapp():

    external_stylesheets = [
        'https://unpkg.com/tailwindcss@^2.0/dist/tailwind.min.css"']
    app = dash.Dash(__name__, meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"}], external_stylesheets=external_stylesheets)
    app.title = 'I2E Dashboard'
    app.config.suppress_callback_exceptions = True
    raw = covert_to_df()
    mapa = get_map(raw)

    datatemp = raw[["Researcher", "Surname",
                    "Organization", "City", "Knowledge"]]
    datatemp = datatemp.drop_duplicates()
    datatemp = datatemp.sort_values(by=["Knowledge"])
    data_dict = datatemp.to_dict('records')

    # traducir a español
    data_table = dash_table.DataTable(
        id='researcher-table',
        data=data_dict,
        columns=[{"name": i, "id": i} for i in datatemp.columns],
        sort_action="native",
        style_cell={'border': '1px solid grey',
                    'textAlign': 'left', 'padding': '5px'},

        style_header={'backgroundColor': '#f8f8f8', 'fontWeight': 'bold'},
        css=[{'selector': '.dash-spreadsheet td div',
              'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'}],
    )
    area = get_knowledge_area_data("Area", raw)
    discipline = get_knowledge_area_data("Disciplina", raw)
    subdiscipline = get_knowledge_area_data("Subdisciplina", raw)
    field = get_knowledge_area_data("Campo", raw)
    subfield = get_knowledge_area_data("Subcampo", raw)
    area_options = get_options(area)
    discipline_options = get_options(discipline)
    subdiscipline_options = get_options(subdiscipline)
    field_options = get_options(field)
    subfield_options = get_options(subfield)

    app.layout = html.Div(className="bg-gray-200	 h-full", children=[
        html.Div(className="container mx-auto py-4", children=[
            html.Div(className="flex justify-between items-center px-4", children=[
                html.Span(className="text-2xl font-bold",
                          children="I2E Dashboard"),
            ]),

            html.Div(className="grid grid-cols-3 gap-4", children=[
                html.Div(className="col-span-2 rounded-lg shadow-md", children=[
                    dcc.Graph(
                        id="map-graph",
                        figure=mapa,
                        config=dict(displayModeBar=False, scrollZoom=True),
                        className="w-full h-100 rounded-lg shadow-md"
                    ),
                ]),

                html.Div(className="col-span-1 rounded-lg shadow-md", children=[
                    dcc.Graph(
                        id="knowledge-area-bar-chart",
                        config=dict(displayModeBar=False, scrollZoom=True),
                        className="w-full h-100 rounded-lg shadow-md",
                    )
                ]),
                html.Div(className="col-span-1 rounded-lg shadow-md", children=[
                    html.Label("Organization"),
                    dcc.Dropdown(
                        id="Organization",
                        options=[{"label": Organization, "value": Organization} for Organization in raw["Organization"].unique(
                        ).tolist() + ["Todas"] if Organization != "Organization"],
                        value="Todas",
                        className="w-full py-2 px-4 rounded-lg shadow-md bg-gray-200"
                    ),
                    html.Label("Tipo de aprendizaje"),
                    dcc.Dropdown(
                        id="learning-type-dropdown",
                        options=[{"label": learning_type, "value": learning_type} for learning_type in raw["KnowledgeType"].unique(
                        ).tolist() + ["Todas"] if learning_type != "KnowledgeDiscipline"],
                        value="Todas",
                        className="w-full py-2 px-4 rounded-lg shadow-md bg-gray-200"
                    ),
                    html.Label("Cuidad"),
                    dcc.Dropdown(
                        id="city-dropdown",
                        options=[{"label": city, "value": city}
                                 for city in raw["City"].unique().tolist() + ["Todas"] if city != "City"],
                        value="Todas",
                        className="w-full py-2 px-4 rounded-lg shadow-md bg-gray-200"
                    ),
                ]),
                html.Div(className="col-span-1 rounded-lg shadow-md", children=[
                    html.Label("Area de conocimiento"),
                    dcc.Dropdown(
                        id="Area",
                        options=area_options,
                        value="Todas",
                        className="w-full py-2 px-4 rounded-lg shadow-md bg-gray-200"
                    ),
                    html.Label("Disciplina"),
                    dcc.Dropdown(
                        id="Discipline",
                        options=discipline_options,
                        value="Todas",
                        className="w-full py-2 px-4 rounded-lg shadow-md bg-gray-200"
                    ),
                    html.Label("Campo"),
                    dcc.Dropdown(
                        id="Field",
                        options=field_options,
                        value="Todas",
                        className="w-full py-2 px-4 rounded-lg shadow-md bg-gray-200"
                    ),
                ]),
                html.Div(className="col-span-1 rounded-lg shadow-md bg-white flex justify-center items-center", children=[
                    html.Div(
                        id='researcher-count', className="text-4xl text-left p-5 font-bold text-gray-700 flex  font-sans hover:font-serif  justify-center "),
                     #add onther div for the button 
                    

                ]),
                html.Div(className="col-span-2 rounded-lg shadow-md bg-white table-auto justify-center ", children=[
                    data_table, 
                    html.Br(),
html.Button("Descargar tabla", id="btn_xlsx",className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline justify-center"),
                    dcc.Download(id="download-dataframe-xlsx"),

                ]),
                html.Div(className="col-span-1 rounded-lg shadow-md", children=[
                    html.Label("Tipos de conocimiento"),
                    dcc.Graph(
                        id="knowledge-type-pie-chart",
                        config=dict(displayModeBar=False, scrollZoom=True),
                        className="w-full h-100 rounded-lg shadow-md",
                    )
                ]),
            ])
        ])
    ])

    @app.callback(
        Output(component_id='researcher-count', component_property='children'),
        [Input(component_id='Organization', component_property='value'),
         Input(component_id='learning-type-dropdown',
               component_property='value'),
         Input(component_id='city-dropdown', component_property='value'),
         Input(component_id='Area', component_property='value'),
         Input(component_id='Discipline', component_property='value'),
         Input(component_id='Field', component_property='value')
         ]
    )
    def update_researcher_count(selected_organization, learning_type, city, area, discipline, field):
        filtered_data = raw
        if selected_organization != 'Todas':
            filtered_data = filtered_data[filtered_data['Organization']
                                          == selected_organization]
        if learning_type != 'Todas':
            filtered_data = filtered_data[filtered_data['KnowledgeType']
                                          == learning_type]
        if city != 'Todas':
            filtered_data = filtered_data[filtered_data['City'] == city]
        if area != 'Todas':
            filtered_data = filtered_data[filtered_data['Knowledge'] == area]
        if discipline != 'Todas':
            filtered_data = filtered_data[filtered_data['Knowledge']
                                          == discipline]
        if field != 'Todas':
            filtered_data = filtered_data[filtered_data['Knowledge'] == field]
        count = len(filtered_data['Researcher'].unique())
        if count == 1:
            return f'{count} Investigador'
        return f'{count} Investigadores'

    @app.callback(
        dash.dependencies.Output("knowledge-area-bar-chart", "figure"),
        [dash.dependencies.Input("learning-type-dropdown", "value"),
         dash.dependencies.Input("Organization", "value"),
         dash.dependencies.Input("city-dropdown", "value"),
         dash.dependencies.Input("Area", "value"),
         dash.dependencies.Input("Discipline", "value"),

         dash.dependencies.Input("Field", "value")])
    def update_knowledge_area_bar_chart(learning_type, selected_organization, city, area, discipline, field):
        filtered_data = raw
        if selected_organization != 'Todas':
            filtered_data = filtered_data[filtered_data['Organization']
                                          == selected_organization]
        if learning_type != 'Todas':
            filtered_data = filtered_data[filtered_data['KnowledgeType']
                                          == learning_type]
        if city != 'Todas':
            filtered_data = filtered_data[filtered_data['City'] == city]
        if area != 'Todas':
            filtered_data = filtered_data[filtered_data['Knowledge'] == area]
        if discipline != 'Todas':
            filtered_data = filtered_data[filtered_data['Knowledge']
                                          == discipline]
        if field != 'Todas':
            filtered_data = filtered_data[filtered_data['Knowledge'] == field]

        df = filtered_data.groupby("Knowledge")["Researcher"].count()

        return {
            "data": [go.Bar(x=df.index, y=df.values)],
            "layout": go.Layout(title="Áreas de Conocimiento", xaxis={"title": "Área de Conocimiento"}, yaxis={"title": "Numero de Investigadores"}, template="seaborn")

        }

    @app.callback(
        dash.dependencies.Output("map-graph", "figure"),
        [dash.dependencies.Input("Organization", "value"), dash.dependencies.Input("city-dropdown", "value")])
    def update_map_Org(Organization, City):
        if Organization == "Todas" and City == "Todas":
            return get_map(raw)
        elif Organization != "Todas" and City == "Todas":
            filter_data = raw[raw['Organization'] == Organization]
            longitude = filter_data['Long'].mean()
            latitude = filter_data['Lat'].mean()
            map_filtered = get_map(filter_data).update_layout(
                mapbox_zoom=10, mapbox_center={"lat": latitude, "lon": longitude})
            return map_filtered

        elif Organization == "Todas" and City != "Todas":
            filter_data = raw[raw['City'] == City]
            longitude = filter_data['Long'].mean()
            latitude = filter_data['Lat'].mean()
            map_filtered = get_map(filter_data).update_layout(
                mapbox_zoom=10, mapbox_center={"lat": latitude, "lon": longitude})
            return map_filtered
        else:
            filter_data = raw[(raw['Organization'] == Organization) & (
                raw['City'] == City)]
            longitude = filter_data['Long'].mean()
            latitude = filter_data['Lat'].mean()
            map_filtered = get_map(filter_data).update_layout(
                mapbox_zoom=10, mapbox_center={"lat": latitude, "lon": longitude})
            return map_filtered

    @app.callback(
        Output(component_id='researcher-table', component_property='data'),
        [Input(component_id='map-graph', component_property='selectedData'),
         Input(component_id='learning-type-dropdown',
               component_property='value'),
         Input(component_id='Organization', component_property='value'),
         Input(component_id='city-dropdown', component_property='value'),
         Input(component_id='Area', component_property='value'),
         Input(component_id='Discipline', component_property='value'),
         Input(component_id='Field', component_property='value')]
    )
    def update_table(selected_data, learning_type, organization, city, area, discipline, field):
        raw.drop_duplicates(subset="Researcher")
        filtered_data = raw

        if selected_data is not None:
            selected_points = [point['customdata']
                               for point in selected_data['points']]
            filtered_data = filtered_data[filtered_data["Organization"].isin(
                selected_points)]
        if learning_type != "Todas":

            filtered_data = filtered_data[filtered_data["KnowledgeType"]
                                          == learning_type]
        if city != "Todas":
            filtered_data = filtered_data[filtered_data["City"] == city]
        if area != "Todas":
            filtered_data = filtered_data[filtered_data["Knowledge"] == area]
        if discipline != "Todas":
            filtered_data = filtered_data[filtered_data["Knowledge"]
                                          == discipline]
        if field != "Todas":
            filtered_data = filtered_data[filtered_data["Knowledge"] == field]
        return filtered_data.to_dict('records')

    @app.callback(
        Output("knowledge-type-pie-chart", "figure"),
        [Input("learning-type-dropdown", "value"),
         Input("Organization", "value"),
         Input("city-dropdown", "value"),
         Input("Area", "value"),
         Input("Discipline", "value"),
         Input("Field", "value")])
    def update_knowledge_type_pie_chart(learning_type, organization, city, area, discipline, field):
        filtered_data = raw
        if learning_type != "Todas":
            filtered_data = filtered_data[filtered_data["KnowledgeType"]
                                          == learning_type]
        if organization != "Todas":
            filtered_data = filtered_data[filtered_data["Organization"]
                                          == organization]
        if city != "Todas":
            filtered_data = filtered_data[filtered_data["City"] == city]
        if area != "Todas":
            filtered_data = filtered_data[filtered_data["Knowledge"] == area]
        if discipline != "Todas":
            filtered_data = filtered_data[filtered_data["Knowledge"]
                                          == discipline]
        if field != "Todas":
            filtered_data = filtered_data[filtered_data["Knowledge"] == field]
        df = filtered_data.groupby("Knowledge")["Researcher"].count()
        return {
            "data": [go.Pie(labels=df.index, values=df.values)],
            "layout": go.Layout(title="Tipos de Conocimiento", template="seaborn")
        }

    @app.callback(
        Output("download-data", "href"),
        [Input("download-button", "n_clicks")],
        [State("researcher-table", "data")],
    )
    @app.callback(
    Output("download-dataframe-xlsx", "data"),
    Input("btn_xlsx", "n_clicks"), 
    State("researcher-table", "data"),
    prevent_initial_call=True,
)
    def func(n_clicks, data):
        data=pd.DataFrame(data)
        
        return dcc.send_data_frame(data.to_excel, "Dash.xlsx")
    return app

# Run the app


if __name__ == '__main__':
    app = getapp()
    app.run_server(debug=True)

from dash import Dash, dash_table
import pandas as pd
from dash import dcc, html


def get_table(df, pathname="/es"):
    # Remove columns that won't be displayed
    df = df.drop(columns=["Lat", "Long", "Id", "País", "Estado"])

    style_table = {
        "fontFamily": '"Roboto", "Helvetica", "Arial", "sans-serif"',
        "overflowX": "auto",
    }
    style_header = {
        "backgroundColor": "#f8f9fa",
        "fontWeight": "500",
        "padding": "0.75rem",
        "borderBottom": "1px solid #dee2e6",
    }
    style_cell = {
        "fontFamily": '"Roboto", "Helvetica", "Arial", "sans-serif"',
        "fontWeight": "400",
        "fontSize": "0.875rem",
        "lineHeight": "1.5",
        "color": "#212529",
        "textAlign": "left",
        "whiteSpace": "normal",
        "height": "auto",
        "padding": "0.75rem",
        "border": "1px solid #dee2e6",
        "verticalAlign": "top",
    }
    style_data_conditional = [
        {
            "if": {"row_index": "odd"},
            "backgroundColor": "rgb(248, 248, 248)",
        }
    ]
    style_cell_conditional = [
        {
            "if": {"column_id": c},
            "textAlign": "left",
        }
        for c in df.columns
    ]

    if pathname == "/en":
        ''' CVU
            Nombre
            Apellido
            SNI
            Ciudad
            Área
            Campos
            Disciplinas
            Institución '''

        columns = [{"name": i, "id": i} for i in df.columns] 
        columns[0]["name"] = "CVU"
        columns[1]["name"] = "Name"
        columns[2]["name"] = "Last Name"
        columns[3]["name"] = "SNI"
        columns[4]["name"] = "City"
        columns[5]["name"] = "Area"
        columns[6]["name"] = "Fields"
        columns[7]["name"] = "Disciplines"
        columns[8]["name"] = "Institution"
            
        style_header["backgroundColor"] = "#f8f9fa"
        style_header["borderBottom"] = "1px solid #dee2e6"
        style_cell["textAlign"] = "left"
        style_data_conditional = []

    else:
        columns = [{"name": i, "id": i} for i in df.columns]

    data_table = dash_table.DataTable(
        id="researcher-table",
        columns=columns,
        data=df.to_dict("records"),
        page_size=7,
        page_action="native",
        filter_action="native",
        sort_action="native",
        sort_mode="single",
        column_selectable="single",
        style_as_list_view=True,
        style_table=style_table,
        style_header=style_header,
        style_cell=style_cell,
        style_data_conditional=style_data_conditional,
        style_cell_conditional=style_cell_conditional,
    )
    return data_table

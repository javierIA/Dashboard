import pandas as pd
import plotly.graph_objs as go
from dash import dcc
from dash import html
import colorlover as cl
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def get_graph(data, pathname="/es"):
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

    # Convertir la lista de diccionarios en un DataFrame de pandas
    df = pd.DataFrame(data)

    # Utilizar groupby para contar el número de elementos para cada tipo
    counts = df.groupby("Tipo").size().reindex(type_count_map.keys()).tolist()

    colors = cl.scales["9"]["qual"]["Paired"]
    colors = cl.interp(colors, len(type_labels))

    if pathname == "/en":
        type_labels = (
            "Scientific Paper",
            "Research Project",
            "Research Group",
            "Patent",
        )
        title = "Papers"
        xaxis_title = "Type"
        yaxis_title = "Number of papers"
    elif pathname == "/es":
        title = "Publicaciones"
        xaxis_title = "Tipo"
        yaxis_title = "Cantidad de publicaciones"

    bar_data = [go.Bar(x=type_labels, y=counts, marker=dict(color=colors))]
    layout = go.Layout(
        title=title,
        xaxis=dict(title=xaxis_title),
        yaxis=dict(title=yaxis_title),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(color="black", size=10),
        margin=dict(l=0, r=0, t=30, b=0),
    )

    return dcc.Graph(id="graph_papers", figure={"data": bar_data, "layout": layout})


def transform_data(data):
    df = pd.DataFrame(data)
    grouped = df.groupby("Área")
    transformed = pd.DataFrame(
        {
            "Área": grouped.mean().index,
            "X": grouped.mean()["X"],
            "Y": grouped.mean()["Y"],
            "Tamaño": grouped.count()["Nombre"],
            "Nombre": grouped["Nombre"].apply(lambda x: ", ".join(x)),
        }
    )
    return transformed


def get_graph_groupBy(data, pathname="/es"):
    print("get_graph_groupBy")
    # Agrupar los datos por área y contar cuántos investigadores hay en cada área
    grouped_data = data.groupby("Área")["Nombre"].count().reset_index()

    # Definir colores para cada área
    colors = cl.scales["12"]["qual"]["Paired"]
    colors = cl.interp(colors, max(1, len(grouped_data["Área"])))
    grouped_data["Nombre"] = grouped_data["Nombre"].astype(str)
    # Extraer las siglas de cada área
    grouped_data["Área"] = grouped_data["Área"].apply(lambda x: x.split(" ")[0])

    if pathname == "/en":
        title = "Number of Researchers by Area"
        xaxis_title = "Area"
        yaxis_title = "Number of Researchers"
    elif pathname == "/es":
        title = "Número de investigadores por área"
        xaxis_title = "Área"
        yaxis_title = "Número de investigadores"

    fig = go.Figure(
        [go.Bar(x=grouped_data["Área"], y=grouped_data["Nombre"], marker_color=colors)]
    )
    fig.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        font=dict(size=14),
        margin=dict(l=0, r=0, t=30, b=0),
    )

    return dcc.Graph(id="graph_areas", figure=fig)

import pandas as pd
import plotly.graph_objs as go
from dash import dcc
from dash import html
import colorlover as cl
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def get_graph(data):
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

    # Convert the list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(data)

    # Use groupby to count the number of elements for each type
    counts = df.groupby("Tipo").size().reindex(type_count_map.keys()).tolist()

    colors = cl.scales["9"]["qual"]["Paired"]
    colors = cl.interp(colors, len(type_labels))

    bar_data = [go.Bar(x=type_labels, y=counts, marker=dict(color=colors))]
    layout = go.Layout(
        xaxis=dict(title="Tipo"),
        yaxis=dict(title="Cantidad"),
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


def get_graph_groupBy(data):
    # Agrupar los datos por área y contar cuántos investigadores hay en cada área
    grouped_data = data.groupby("Área")["Nombre"].count().reset_index()

    # Definir colores para cada área
    colors = cl.scales["12"]["qual"]["Paired"]
    colors = cl.interp(colors, max(1, len(grouped_data["Área"])))
    grouped_data["Nombre"] = grouped_data["Nombre"].astype(str)
    # extrer las siglas de cada área
    grouped_data["Área"] = grouped_data["Área"].apply(lambda x: x.split(" ")[0])
    # Crear el gráfico si color es negro tomar el color de la lista de colores
    fig = go.Figure(
        [go.Bar(x=grouped_data["Área"], y=grouped_data["Nombre"], marker_color=colors)]
    )
    fig.update_layout(
        title="Número de investigadores por área",
        xaxis_title="Área",
        yaxis_title="Número de investigadores",
        font=dict(size=14),
        margin=dict(l=0, r=0, t=30, b=0),
    )

    # Mostrar el gráfico
    return dcc.Graph(id="graph_areas", figure=fig)

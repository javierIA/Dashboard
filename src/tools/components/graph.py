import pandas as pd
import plotly.graph_objs as go
from dash import dcc
from dash import html
import colorlover as cl


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
        font=dict(color="black"),
    )

    return dcc.Graph(id="graph_papers", figure={"data": bar_data, "layout": layout})

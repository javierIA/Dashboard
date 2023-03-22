import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import utils
import pandas as pd
from pathlib import Path


def get_map(researchers, institutions):
    data = pd.concat([researchers, institutions], sort=False).reset_index(drop=True)

    # Agregar una columna 'Tipo' que indica si cada fila representa un investigador o una institución
    data["Tipo"] = data["Institución"].apply(
        lambda x: "Institución" if isinstance(x, str) else "Investigador"
    )

    # Cargar los límites geográficos del estado
    statejson = Path(__file__).parent.parent.parent.joinpath("assets", "chihuahua.json")
    with open(statejson, encoding="utf8") as f:
        provinces_map = json.load(f)
    # Configurar el token de acceso a Mapbox
    px.set_mapbox_access_token(
        "pk.eyJ1IjoiamF2aWVmbG84OCIsImEiOiJjbGNwdmk0bmQ0bHBsM3FwNDF5Z2hxdHo3In0.WWUNSAWH-v4mgpBAlFFR5A"
    )
    # Crear la figura del mapa
    fig = px.scatter_mapbox(
        data,
        lat="Lat",
        lon="Long",
        hover_name="Nombre",
        hover_data=["Institución"],
        color="Tipo",
        color_discrete_map={
            "Investigador": "rgb(255,92,147)",
            "Institución": "rgb(52, 207, 93)",
        },
        zoom=5,
        height=600,
        mapbox_style="carto-positron",
        center={"lat": 28.635308, "lon": -106.088875},
        opacity=0.7,
        labels={"Tipo": "Tipo de entidad"},
    )

    fig.update_layout(
        mapbox_style="carto-positron",
        hovermode="closest",
        showlegend=False,
        mapbox=dict(
            bearing=4,
            center=dict(lat=28.635308, lon=-106.088747),
            pitch=30,
            zoom=6,
            layers=[
                dict(
                    sourcetype="geojson",
                    source=provinces_map,
                    type="fill",
                    color="rgba(100,108,255, 0.4)",
                    below="traces",
                )
            ],
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        mapbox_bounds={"west": -180, "east": -50, "south": 20, "north": 90},
        uirevision=True,
    )
    fig.add_trace(
        go.Scattermapbox(
            lat=data["Lat"],
            lon=data["Long"],
            hoverinfo="text",
            hoverlabel=dict(
                bgcolor="white", bordercolor="black", font=dict(color="black", size=20)
            ),
            hovertemplate="<b>%{hovertext}</b><br><br>",
            hovertext=data.apply(
                lambda row: row["Institución"]
                if row["Tipo"] == "Institución"
                else row["Nombre"],
                axis=1,
            ),
            mode="markers + text",
            marker=go.scattermapbox.Marker(
                size=15,
                color=data["Tipo"].apply(
                    lambda x: "rgb(255,92,147)"
                    if x == "Investigador"
                    else "rgb(52, 207, 93)"
                ),
                opacity=0.7,
                symbol="circle",
            ),
            texttemplate="%{hovertext}",
            textposition="bottom center",
            textfont=dict(size=10, color="black"),
            text=data.apply(
                lambda row: row["Institución"]
                if row["Tipo"] == "Institución"
                else row["Nombre"],
                axis=1,
            ),
        )
    )
    fig.update_traces(cluster=dict(maxzoom=20, opacity=0.9, step=4))

    return fig

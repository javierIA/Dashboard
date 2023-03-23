import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import pandas as pd
from pathlib import Path


def get_map(
    researchers, institutions, zoom=6, center={"lat": 28.635308, "lon": -106.088747}
):
    data = pd.concat([researchers, institutions], sort=False).reset_index(drop=True)
    data["Tipo"] = data["CVU"].apply(
        lambda x: "Investigadores" if isinstance(x, str) else "Institución"
    )
    records_count = (
        data.groupby(["Lat", "Long"]).size().reset_index(name="Num_registros")
    )
    data = pd.merge(data, records_count, on=["Lat", "Long"])
    data["Institución"] = data["Institución"].apply(
        lambda x: x.split(",") if isinstance(x, str) else x
    )

    # Then, explode the 'Institución' field to create a new row for each institution
    data = data.explode("Institución").reset_index(drop=True)
    statejson = Path(__file__).parent.parent.parent.joinpath("assets", "chihuahua.json")

    with open(statejson, encoding="utf8") as f:
        provinces_map = json.load(f)
    px.set_mapbox_access_token(
        "pk.eyJ1IjoiamF2aWVmbG84OCIsImEiOiJjbGNwdmk0bmQ0bHBsM3FwNDF5Z2hxdHo3In0.WWUNSAWH-v4mgpBAlFFR5A"
    )
    mapbox_access_token = "pk.eyJ1IjoiamF2aWVmbG84OCIsImEiOiJjbGNwdmk0bmQ0bHBsM3FwNDF5Z2hxdHo3In0.WWUNSAWH-v4mgpBAlFFR5A"
    fig = px.scatter_mapbox(
        data,
        lat="Lat",
        lon="Long",
        hover_name="Nombre",
        hover_data=["Institución"],
        color="Tipo",
        color_discrete_map={
            "Investigadores": "rgb(255,92,147)",
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
        showlegend=False,
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=-3,
            center=center,
            zoom=zoom,
            pitch=20,
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
    )

    fig.add_trace(
        go.Scattermapbox(
            lat=data["Lat"],
            lon=data["Long"],
            hoverinfo="text",
            hoverlabel=dict(
                bgcolor="white", bordercolor="black", font=dict(color="black", size=20)
            ),
            hovertemplate="<b>%{hovertext}</b> - <i> Registros : %{customdata}</i>",
            customdata=data.apply(
                lambda row: row["Registrados"]
                if row["Tipo"] == "Institución"
                else row["Num_registros"],
                axis=1,
            ),
            hovertext=data.apply(
                lambda row: row["Nombre"]
                if row["Tipo"] == "Institución"
                else row["Tipo"],
                axis=1,
            ),
            mode="markers",
            marker=go.scattermapbox.Marker(
                size=25,
                color=data["Tipo"].apply(
                    lambda x: "rgb(255,92,147)"
                    if x == "Investigadores"
                    else "rgb(52, 207, 93)"
                ),
                opacity=0.7,
                symbol="circle",
            ),
            showlegend=False,
        )
    )
    fig.update_traces(cluster=dict(maxzoom=9, opacity=0.8, step=4))

    return fig

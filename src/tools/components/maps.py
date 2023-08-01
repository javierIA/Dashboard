import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash import Dash, html
import pandas as pd
from dash_extensions.javascript import Namespace


def prepare_data(researchers, institutions):
    researchers["Tipo"] = "Investigadores"
    institutions["Tipo"] = "Institución"
    data = pd.concat([researchers, institutions], sort=False).reset_index(drop=True)
    data["tooltip"] = data["Nombre"] + " (" + data["Tipo"] + ")"
    records_count = (
        data.groupby(["Lat", "Long"]).size().reset_index(name="Num_registros")
    )
    data = pd.merge(data, records_count, on=["Lat", "Long"])
    return data


def clean_data(data, default_lat=28.635308, default_lon=-106.088747):
    data["Lat"] = pd.to_numeric(data["Lat"], errors="coerce")
    data["Long"] = pd.to_numeric(data["Long"], errors="coerce")
    data["tooltip"] = (
        data["Nombre"]
        + " ("
        + data["Tipo"]
        + ") - "
        + data["Num_registros"].astype(str)
        + " registros"
    )
    data = data.dropna(subset=["Lat", "Long"])
    data["Ciudad"] = data["Ciudad"].fillna("Desconocido")
    data["Lat"].fillna(default_lat, inplace=True)
    data["Long"].fillna(default_lon, inplace=True)
    return data


def get_grouped_data(data):
    return (
        data.groupby("Ciudad")
        .agg(
            Num_registros=pd.NamedAgg(column="Num_registros", aggfunc="sum"),
            avg_lat=pd.NamedAgg(column="Lat", aggfunc="mean"),
            avg_lon=pd.NamedAgg(column="Long", aggfunc="mean"),
        )
        .reset_index()
    )


def get_info():
    return [
        html.H4("Information"),
        html.P("This map visualizes the locations of researchers and institutions."),
    ]


def get_map(researchers, institutions, zoom=6, center=[28.635308, -106.088747]):
    attribution = "IA.CENTER 2023"
    colorscale = ["red", "yellow", "green", "blue", "purple"]
    color_prop = "Num_registros"
    ns = Namespace("myNamespace", "mySubNamespace")

    data = prepare_data(researchers, institutions)
    vmax = data["Num_registros"].max()
    data = clean_data(data)
    grouped = get_grouped_data(data)
    minicharts = []
    for index, row in grouped.iterrows():
        # The pie chart will have two slices: one representing Num_registros, and the other slice representing the maximum value minus Num_registros.
        chart_data = [row["Num_registros"], vmax - row["Num_registros"]]

        popup_content = f"Ciudad: {row['Ciudad']}, Records: {row['Num_registros']}"
        popup = dl.Popup(children=popup_content)

        minichart = dl.LayerGroup(
            children=[
                dl.Minichart(
                    lat=row["avg_lat"], lon=row["avg_lon"], type="pie", data=chart_data
                ),
                popup,
            ]
        )
        minicharts.append(minichart)
    dicts = data[
        ["Lat", "Long", "Nombre", "Num_registros", "tooltip", "Ciudad", "Tipo"]
    ].to_dict("rows")

    geojson = dlx.dicts_to_geojson(dicts, lat="Lat", lon="Long")
    geobuf = dlx.geojson_to_geobuf(geojson)

    # Lógica de renderización
    colorbar = dl.Colorbar(
        colorscale=colorscale, width=20, height=150, min=0, max=vmax, unit="registros"
    )
    chihuahua = dl.GeoJSON(
        url="/assets/chihuahua.json",
        id="chihuahua",
        options=dict(
            style=dict(
                color="rgba(100,108,255, 0.6)",
                options=dict(
                    fillColor="rgba(100,108,255, 0.4)",
                    fillOpacity=0.7,
                    weight=10,
                    opacity=0.7,
                ),
                weight=2,  # Grosor del borde
                opacity=0.5,
                # Opacidad del borde
            )
        ),
    )

    geojson = dl.GeoJSON(
        data=geobuf,
        id="geojson",
        zoomToBounds=True,
        format="geobuf",
        cluster=True,
        zoomToBoundsOnClick=True,
        superClusterOptions=dict(radius=20),
        hideout=dict(
            colorProp=color_prop,
            circleOptions=dict(fillOpacity=1, stroke=False, radius=5),
            min=0,
            max=vmax,
            colorscale=colorscale,
        ),
        # Use the namespace here
    )
    info = html.Div(
        children=get_info(),
        id="info",
        className="info",
        style={
            "position": "absolute",
            "top": "10px",
            "right": "10px",
            "z-index": "1000",
        },
    )
    return dl.Map(
        children=[
            dl.TileLayer(
                url="https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png",
                maxZoom=20,
                attribution=attribution,
            ),
            geojson,
            chihuahua,
            colorbar,
            info,
            dl.LocateControl(options={"locateOptions": {"enableHighAccuracy": True}}),
        ],
        center=center,
        zoom=zoom,
        style={"width": "100%", "height": "70vh"},
    )

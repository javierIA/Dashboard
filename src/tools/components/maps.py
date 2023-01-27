import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import utils
import pandas as pd
from pathlib import Path


def get_map(df):
    data = df
    statejson = Path(__file__).parent.parent.parent.joinpath(
        'assets', 'chihuahua.json')
    with open(statejson, encoding='utf8') as f:
        provinces_map = json.load(f)
    px.set_mapbox_access_token(
        "eyJ1IjoiamF2aWVmbG84OCIsImEiOiJjbGNwdmk0bmQ0bHBsM3FwNDF5Z2hxdHo3In0")
    fig = go.Figure()
    fig.add_trace(


        go.Scattermapbox(
            lat=data['Lat'],
            lon=data['Long'],
            hoverinfo='text',
            hoverlabel=dict(bgcolor="white",   bordercolor="black",
                            font=dict(color="black", size=20)),
            hovertemplate="<b>%{hovertext}</b><br><br>",
            hovertext=data['Organization'],
            mode="markers",
            marker=go.scattermapbox.Marker(
                size=15,
                color='rgb(255,92,147)',

                opacity=0.7
            ),


        ))

    fig.update_layout(mapbox_style="carto-positron",

                      hovermode='closest',
                      showlegend=False,

                      mapbox=dict(
                          bearing=2,

                          center=dict(
                              lat=28.635308,
                              lon=-106.088747
                          ),
                          pitch=34,
                          zoom=6,
                          layers=[
                              dict(
                                  sourcetype='geojson',
                                  source=provinces_map,
                                  type='fill',
                                  color='rgba(100,108,255, 0.4)',
                                  below="traces"

                              )
                          ],


                      ),

                      )

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_layout(
        mapbox_bounds={"west": -180, "east": -50, "south": 20, "north": 90})
    return fig

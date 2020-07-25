# from opensky_api import OpenSkyApi

# organize imports by inlcuded, installed, then alphabetical / plotly own block due to volume
import json

from utils import Coords, Plane

import numpy as np
import matplotlib.pyplot as plt
import requests

import plotly.express as px
import plotly.graph_objects as go


def main():
# classes first, then execute code
# for modular code, put code in a main function

    r = requests.get("https://opensky-network.org/api/states/all?lamin=36&lomin=-124&lamax=39&lomax=-121")
    rest = r.json()
    states = rest['states']
    tracks = [] # will hold the Planes from the opensky data

    for trk in states:
        if not trk[8]: #filters tracks that are squawking on the ground
            tracks.append(Plane(trk[6], trk[5], trk[10], trk[9], trk[1]))

    time = input("prediction time in minutes >>> ")

    for trk in tracks:
        print()
        print(f"      **** {trk.callsign.strip()} ****")
        print(f"currently at:  {str(trk.coords)}")
        print("heading " + str(trk.hdg) + "deg, at " + str(trk.vel) + "m/s")
        print("will be at: " + str(trk.predict(int(time))))

    paths = [] # will hold plotly info

    for i in range(len(tracks)):
        paths.append(
            go.Scattergeo(
                locationmode='USA-states',
                lon=[tracks[i].lon, tracks[i].predict(int(time)).lon],
                lat=[tracks[i].lat, tracks[i].predict(int(time)).lat],
                mode='lines+markers',
                line=dict(width=1, color='red'),
                marker={'symbol':  [2,0],'size': 7, 'color': "red"},
                opacity=float(tracks[i].vel/max(tracks, key=lambda x: x.vel).vel),
                hoverinfo='text',
                text=tracks[i].callsign
                ))

    layout = go.Layout(
        autosize=True,
        showlegend=False,
        geo=go.layout.Geo(
            resolution = 50,
            showcoastlines=True,
            scope = 'north america',
            projection = go.layout.geo.Projection(
                type = 'orthographic',
                ),
            )
        )

    fig = go.Figure(data = paths, layout = layout)
    fig.update_geos(fitbounds='locations')
    fig.show()


if __name__ == '__main__':
    main()

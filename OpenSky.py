# from opensky_api import OpenSkyApi
import requests
import json
from math import radians, degrees, asin, sin, cos, atan2
import numpy as np

# api = OpenSkyApi()
# s = api.get_states() 
# s = api.get_states(bbox=(36,40,-118,-124))
# states = s.states

r = requests.get("https://opensky-network.org/api/states/all")

rest = r.json()
states = rest['states']

tracks = []

class Coords:
    def __init__(self, lat: float, lon: float):
        self.latString = "{:.2f}".format(lat)
        self.longString = "{:.2f}".format(lon)
        self.lat = radians(lat)
        self.lon = radians(lon)

    def __repr__(self):
        if self.lon < 0:
            return "N " + self.latString + " W " + self.longString
        else:
            return "N " + self.latString + " E " + self.longString

class Plane:
    def __init__(self, lat, lon, hdg, vel, callsign="Unk"):
        self.lat = lat
        self.lon = lon
        self.hdg = hdg
        self.vel = vel
        self.callsign = callsign
        # self.coords = Coords(self.lat, self.lon)

    def __repr__(self):
        return f"({self.lat}, {self.lon}, {self.hdg}, {self.vel}, {self.callsign})"

    def predict(self, time=60): # this is broken...check equation or use API...
        r = 3958.8 # radius in miles
        brg = radians(self.hdg)
        dist = time * self.vel * 2.23694 / 60 / 60
        startLat = self.lat
        startLong = self.lon
        endLat = asin(sin(startLat)*cos(dist/r) + cos(startLat)*sin(dist/r)*cos(brg))
        endLong = startLong + atan2(sin(brg)*sin(dist/r)*cos(startLat),cos(dist/r)-sin(startLat)*sin(endLat))
        endCoords = Coords(degrees(endLat),degrees(endLong))
        return endCoords

for trk in states:
    tracks.append(Plane(trk[5], trk[6], trk[10], trk[9], trk[1]))

rando = tracks[np.random.randint(0,len(tracks))]
print(rando)
# print("currently at: " + rando.coords)
print(rando.predict())
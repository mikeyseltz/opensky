from opensky_api import OpenSkyApi

api = OpenSkyApi()
s = api.get_states()
# s = api.get_states(bbox=(36,40,-118,-124))
states = s.states

tracks = []

class Plane:
	def __init__(self, lat, lon, hdg, vel, callsign="Unk"):
		self.lat = lat
		self.long = lon
		self.hdg = hdg
		self.vel = vel
		self.callsign = callsign

	def __repr__(self):
		return self.callsign + "/ heading: " + str(self.hdg)

	def predict(time=60):
		pass

for trk in states:
	tracks.append(Plane(trk.latitude, trk.longitude, trk.heading, trk.velocity, trk.callsign))

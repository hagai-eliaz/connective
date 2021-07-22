import googlemaps
import haversine as hs
from haversine import Unit

API_KEY = "AIzaSyDKkYpjJONrNZN-BtOXR7ZhSEqSI4pnSdo"


def check_google_distance(loc1, loc2):
    gmaps = googlemaps.Client(key=API_KEY)
    result = gmaps.distance_matrix(loc1, loc2, mode="driving")
    try:
        return True, result["rows"][0]["elements"][0]["distance"]["value"]
    except KeyError:
        return False, result["rows"][0]["elements"][0]["distance"]["value"]


def check_linear_distance(loc1, loc2):
    return hs.haversine(loc1, loc2, unit=Unit.KILOMETERS)

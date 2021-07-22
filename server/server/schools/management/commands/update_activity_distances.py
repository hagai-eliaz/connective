import googlemaps
import haversine as hs
from django.core.management.base import BaseCommand
from haversine import Unit

from server.organizations.models import Activity
from server.schools.models import School


class Command(BaseCommand):
    API_KEY = "AIzaSyDKkYpjJONrNZN-BtOXR7ZhSEqSI4pnSdo"
    ACTIVITY_DICT = {
        "5_and_less": {},
        "10_and_less": {},
        "15_and_less": {},
        "20_and_less": {},
        "25_and_less": {},
        "30_and_less": {},
    }
    help = "Updates the activity distance cache for schools"

    def add_arguments(self, parser):
        "parser.add_argument('some_number', nargs='+', type=int)"
        pass

    def __check_google_distance(self, loc1, loc2):
        gmaps = googlemaps.Client(key=self.API_KEY)
        result = gmaps.distance_matrix(loc1, loc2, mode="driving")
        try:
            return True, result["rows"][0]["elements"][0]["duration"]["value"]
        except KeyError:
            return False, result["rows"][0]["elements"][0]["duration"]["value"]

    def __check_linear_distance(self, school_coords, org_location):
        return hs.haversine(school_coords, org_location, unit=Unit.KILOMETERS)

    def create_all(self, school):
        for activity in Activity.objects.all():
            org_location = tuple(float(coord) for coord in activity.location.split(","))
            school_coords = tuple(float(coord) for coord in school.location.split(","))
            free_distance = self.__check_linear_distance(school_coords, org_location)
            if free_distance < 5:
                google_status = self.__check_google_distance(
                    school_coords, org_location
                )
                self.ACTIVITY_DICT["5_and_less"][activity.slug] = {
                    "google_distance": google_status[0],
                    "distance": google_status[1],
                }
            elif free_distance < 10:
                self.ACTIVITY_DICT["10_and_less"][activity.slug] = {
                    "google_distance": False,
                    "distance": free_distance,
                }
            elif free_distance < 15:
                self.ACTIVITY_DICT["15_and_less"][activity.slug] = {
                    "google_distance": False,
                    "distance": free_distance,
                }
            elif free_distance < 20:
                self.ACTIVITY_DICT["20_and_less"][activity.slug] = {
                    "google_distance": False,
                    "distance": free_distance,
                }
            elif free_distance < 25:
                self.ACTIVITY_DICT["25_and_less"][activity.slug] = {
                    "google_distance": False,
                    "distance": free_distance,
                }
            elif free_distance < 30:
                self.ACTIVITY_DICT["30_and_less"][activity.slug] = {
                    "google_distance": False,
                    "distance": free_distance,
                }

        return self.ACTIVITY_DICT

    def handle(self, *args, **options):
        for school in School.objects.all():
            distance_cache = self.create_all(school)
            import pdb

            pdb.set_trace()
            school.activity_distance_cache = distance_cache
            school.save()

"""
Timezone lookup with tzwhere
"""
from tzwhere import tzwhere

class TimezoneFinder(object):
    """
    Class that looks up timezone for coordinates
    """

    def __init__(self):
        self.timezone_finder = tzwhere.tzwhere(forceTZ=True)

    def timezone_lookup(self, lon, lat):
        """
        Given a longitude and latitude, return the timezone
        """
        # Use an error of 0.045 degrees (roughly 5km) in case tzwhere needs to search
        # nearby polygons for timezones
        return self.timezone_finder.tzNameAt(latitude=float(lat), longitude=float(lon),
                                             forceTZ=True, delta_degrees=0.045)

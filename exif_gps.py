import exifread

# based on https://gist.github.com/erans/983821

def _get_if_exist(data, key):
    if key in data:
        return data[key]

    return None


def _convert_to_degress(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format

    :param value:
    :type value: exifread.utils.Ratio
    :rtype: float
    """
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)
    
def get_exif_location(exif_data):
    """
    Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)
    """
    lat = None
    lon = None

    gps_latitude = _get_if_exist(exif_data, 'GPS GPSLatitude')
    gps_latitude_ref = _get_if_exist(exif_data, 'GPS GPSLatitudeRef')
    gps_longitude = _get_if_exist(exif_data, 'GPS GPSLongitude')
    gps_longitude_ref = _get_if_exist(exif_data, 'GPS GPSLongitudeRef')

    if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
        lat = _convert_to_degress(gps_latitude)
        if gps_latitude_ref.values[0] != 'N':
            lat = 0 - lat

        lon = _convert_to_degress(gps_longitude)
        if gps_longitude_ref.values[0] != 'E':
            lon = 0 - lon

    return lat, lon


# fn = 'IMG_9119.JPG'
# fn = '1594607135608049.jpg'
fn = 'IMG_9101.mp4'
# f = open(fn, 'rb')
# tags = exifread.process_file(f)
# print tags
# lat, long = get_exif_location(tags)
#
# from geopy.geocoders import Nominatim
# locator = Nominatim(user_agent="myGeocoder")
# coordinates = "%s, %s" % (lat, long)
# location = locator.reverse(coordinates)
# print(location.raw)

# from exiftool import ExifTool
# e = ExifTool()
# e.start()
# e.get_metadata(fn)

import subprocess
import os
import re
file = os.path.join(os.getcwd(),"photos",fn)
file = "C:\\Users\\Jade Pham\\PycharmProjects\\Classifier\\photos\\1594609851295618.jpg"
file = "C:\\Users\\Jade Pham\\PycharmProjects\\Classifier\\photos\\1594607135608049.jpg"
file = "C:\\Users\\Jade Pham\\PycharmProjects\\Classifier\\photos\\1594609860964373.jpg"
file = "C:\\Users\\Jade Pham\\PycharmProjects\\Classifier\\photos\\apple_iphone_11_pro_10.jpg"
_cmd = "exiftool -c \"%.6f degrees\" \"" + file + "\""
print _cmd
result = subprocess.Popen(_cmd, shell=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)

output, error = result.communicate()
print output
print error
_re = re.search(".*GPS Position\s+:\s(.*) degrees (.*), (.*) degrees (.*)", output)
lat = _re.group(1)
lat_d = _re.group(2)
long = _re.group(3)
long_d = _re.group(4)
print lat
print long

from geopy.geocoders import Nominatim
# locator = Nominatim(user_agent="myGeocoder")
# locator = Nominatim(user_agent="http")
# coordinates = "%s %s, %s %s" % (lat, lat_d, long, long_d)
# location = locator.reverse(coordinates)
# print(location.raw)
# print(dir(location))
# print location.raw['address']['country']
# print location.raw['address']['suburb']

from datetime import datetime
timestamp = os.path.getctime(file)
print timestamp
date_time = datetime.fromtimestamp(timestamp)
print date_time.strftime("%Y-%B-%d %H:%M:%S")
year = date_time.strftime("%Y")
month = date_time.strftime("%B")
date = date_time.strftime("%Y-%m-%d")
print year
print date
print month

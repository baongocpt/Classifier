# https://pypi.org/project/trackanimation/
# https://towardsdatascience.com/reverse-geocoding-in-python-a915acf29eb6
# https://pypi.org/project/ExifRead/


from GPSPhoto import gpsphoto
import geopy

# fn = 'C:/Users/FSIN/Desktop/photos_test/apple_iphone_11_pro_10.jpg'
# fn = 'C:/Users/FSIN/Desktop/photos_test/IMG_9119.JPG'

# fn = 'C:/Users/FSIN/Desktop/photos_test/IMG_9101.mp4'
# fn = 'C:/Users/FSIN/Desktop/photos_test/IMG_9069.JPG'
# fn = 'C:/Users/FSIN/Desktop/photos_test/IMG_9074.JPG'
# new_fn = 'C:/Users/FSIN/Desktop/new_apple_iphone_11_pro_08.jpg'
fn = '/Users/ngocpham/Desktop/test_image/input/IMG_7663.JPG'
fn = '/Users/ngocpham/Desktop/test_image/input/IMG_7621.JPG'
print fn
# Get the data from image file and return a dictionary
data = gpsphoto.getGPSData(fn)
# rawData = gpsphoto.getRawData(fn)
# print rawData

# Print out just GPS Data of interest
# for tag in data.keys():
#     print "%s: %s" % (tag, data[tag])

# Print out raw GPS Data for debugging
# for tag in rawData.keys():
#     print "%s: %s" % (tag, rawData[tag])

lat = data['Latitude']
alt = data['Altitude']
long = data['Longitude']
print lat
print alt
print long

from geopy.geocoders import Nominatim
locator = Nominatim(user_agent="myGeocoder")
coordinates = "%s, %s" % (lat, long)
location = locator.reverse(coordinates)
print(location.raw.keys())
# print location.raw['display_name']
# print location.raw['place_id']
# print location.raw['lon']
# print location.raw['boundingbox']
# print location.raw['osm_type']
# print location.raw['licence']
# print location.raw['osm_id']
# print location.raw['lat']
print location.raw['address']

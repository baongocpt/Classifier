import os
import re
import subprocess
from datetime import datetime
from geopy.geocoders import Nominatim


def format_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp)


class Media:
    def __init__(self, path):
        self.path = path
        self.latitude = None
        self.latitude_direction = None
        self.longitude = None
        self.longitude_direction = None
        self.country = ''
        self.county = ''
        self.suburb = ''
        self.city = ''
        self.town = ''
        self.state = ''
        self.amenity = ''

    def load_info(self):
        self.load_details()
        self.load_metadata()

    def load_details(self):
        created_timestamp = os.path.getctime(self.path)
        modified_timestamp = os.path.getmtime(self.path)
        self.file_size = os.path.getsize(self.path)
        self.created_time = format_timestamp(created_timestamp)
        self.modified_time = format_timestamp(modified_timestamp)
        self.modified_year = self.modified_time.strftime("%Y")
        self.modified_month = self.modified_time.strftime("%B")
        self.modified_date = self.modified_time.strftime("%Y-%m-%d")

    def load_metadata(self):
        try:
            self.get_metadata()
            locator = Nominatim(user_agent="http")
            coordinates = "%s %s, %s %s" % (
                self.latitude, self.latitude_direction,
                self.longitude, self.longitude_direction)
            location = locator.reverse(coordinates)
            if "HTTP Error 400" not in location:
                address = location.raw.get('address')
                print address
                if address.get('country'):
                    self.country = address.get('country').encode('utf-8')
                if address.get('county'):
                    self.county = address.get('county').encode('utf-8')
                if address.get('suburb'):
                    self.suburb = address.get('suburb').encode('utf-8')
                if address.get('city'):
                    self.city = address.get('city').encode('utf-8')
                if address.get('town'):
                    self.town = address.get('town').encode('utf-8')
                if address.get('state'):
                    self.state = address.get('state').encode('utf-8')
                if address.get('amenity'):
                    self.amenity = address.get('amenity').encode('utf-8')
        except Exception as msg:
            print msg

    def get_metadata(self):
        try:
            _cmd = "exiftool -c \"%.6f degrees\" \"" + self.path + "\""
            result = subprocess.Popen(_cmd, shell=True,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
            output, error = result.communicate()
            _re = re.search(".*GPS Position\s+:\s(.*) degrees (.*), (.*) degrees (.*)", output)
            if _re:
                self.latitude = _re.group(1)
                self.latitude_direction = _re.group(2)
                self.longitude = _re.group(3)
                self.longitude_direction = _re.group(4)
        except Exception as msg:
            print msg


if __name__ == '__main__':
    path = '/Users/ngocpham/Desktop/PythonProjects/test_image/input'
    files = os.listdir(path)
    import csv
    csv_file = open('test.csv', 'w')
    writer = csv.writer(csv_file)
    writer.writerow(["Country", "State", "County", "City", "Town", "Suburb", "Amenity"])
    for f in files:
        print f
        file_path = os.path.join(path, f)
        # file_path = '/Users/ngocpham/Desktop/test_image/input/IMG_7630.JPG'
        m = Media(path=file_path)
        m.load_info()
        # print m.created_time
        # print m.modified_time
        # print m.modified_year
        # print m.modified_month
        # print m.modified_date
        print m.country

        print m.state
        print m.county
        print m.city

        print m.town
        print m.town
        print m.city



        print m.suburb

        print m.amenity

        writer.writerow([m.country, m.state, m.county, m.city,
                         m.town, m.suburb,
                         m.amenity])
        print m.latitude
        print m.longitude
    csv_file.close()
    import geocoder

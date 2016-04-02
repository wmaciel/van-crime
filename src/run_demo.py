__author__ = 'walthermaciel'

from geopy.geocoders import DataBC
from geopy.exc import GeopyError
from time import sleep
import sys
from ssl import SSLError
from create_feature_vector import  create_vector
import pandas as pd


def run_demo():
    geolocator = DataBC()

    print '''
888     888                   .d8888b.          d8b
888     888                  d88P  Y88b         Y8P
888     888                  888    888
Y88b   d88P 8888b.  88888b.  888        888d888 888 88888b.d88b.   .d88b.
 Y88b d88P     "88b 888 "88b 888        888P"   888 888 "888 "88b d8P  Y8b
  Y88o88P  .d888888 888  888 888    888 888     888 888  888  888 88888888
   Y888P   888  888 888  888 Y88b  d88P 888     888 888  888  888 Y8b.
    Y8P    "Y888888 888  888  "Y8888P"  888     888 888  888  888  "Y8888


    '''

    print 'Year:'
    year = sys.stdin.readline().strip()

    month_ok = False
    while not month_ok:
        print 'Month:'
        month = sys.stdin.readline().strip()
        if 12 >= int(month) > 0:
            month_ok = True
        else:
            print 'Nice try, champ...'

    print 'Street Name:'
    st_name = sys.stdin.readline().strip()

    print 'Street Number:'
    st_num = sys.stdin.readline().strip()

    address = st_num + ' ' + st_name + ', Vancouver, BC, Canada'

    print 'Researching lat long for ' + address + '...'

    got_it = False
    delay = 1
    while not got_it:
        if delay > 10:
            print 'could not find address, exiting...'
            exit()

        try:
            sleep(delay)
            location = geolocator.geocode(address)
            got_it = True
        except (GeopyError, SSLError) as e:
            delay *= 2
            got_it = False
            print '!!! Are you sure you got the right address? Trying again...'

    print 'Got it!'

    latitude = "{:.8f}".format(location.latitude)
    longitude = "{:.8f}".format(location.longitude)
    print 'LatLong:\t( ' + latitude + ', ' + longitude + ' )'

    print 'Generating feature vector...'
    f_vec = create_vector(int(year), int(month), location.latitude, location.longitude)

    print 'Done!'

if __name__ == '__main__':
    run_demo()

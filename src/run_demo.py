__author__ = 'walthermaciel'

from geopy.geocoders import DataBC
from geopy.exc import GeopyError
from time import sleep
import sys
from ssl import SSLError
from create_feature_vector import  create_vector
import os
import pandas as pd
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier

crime_id = {0: 'BNE Residential   ',
            1: 'Theft from Vehicle',
            2: 'Other Thefts      ',
            3: 'Mischief          ',
            4: 'Theft of Vehicle  ',
            5: 'BNE Commercial    '}

def gather_time():
    print 'Year:\t',
    year = sys.stdin.readline().strip()

    month_ok = False
    while not month_ok:
        print 'Month:\t',
        month = sys.stdin.readline().strip()
        if 12 >= int(month) > 0:
            month_ok = True
        else:
            print 'Nice try, champ...'

    return int(year), int(month)


def gather_address():
    print 'Street Number:\t',
    st_num = sys.stdin.readline().strip()
    
    print 'Street Name:\t',
    st_name = sys.stdin.readline().strip()

    address = st_num + ' ' + st_name + ', Vancouver, BC, Canada'

    return address


def gather_lat_long(address):
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

    return location.latitude, location.longitude


def run_demo():

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
    year, month = gather_time()
    address = gather_address()
    latitude, longitude = gather_lat_long(address)

    print 'Generating feature vector...',
    f_vec = create_vector(int(year), int(month), latitude, longitude)
    print 'OK'


    print 'Loading model...',
    clf = joblib.load('../models/random_forest_model.p')
    print 'OK'

    print '\n\n----- Results -----\n'

    print 'Probability of crime type, given that a crime happened:'
    prob_list = clf.predict_proba(f_vec.as_matrix())[0]
    for i, p in enumerate(prob_list):
        print crime_id[i] + '\t' + "{:.2f}".format(p * 100) + '%'


if __name__ == '__main__':
    geolocator = DataBC()

    while True:
        run_demo()
        print 'press enter to reset'
        sys.stdin.readline()
        os.system('clear')

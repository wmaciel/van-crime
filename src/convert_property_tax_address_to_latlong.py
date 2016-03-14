__author__ = 'walthermaciel'

from geopy.geocoders import DataBC
from geopy.exc import GeopyError
from time import sleep
import sys
import csv
import random
from ssl import SSLError
import os.path

local_db = {}

def main(path_in):
    geolocator = DataBC()
    print 'loading', path_in
    fpin = open(path_in, 'r')

    reader = csv.DictReader(fpin)
    d_list = []
    for row in reader:
        d = dict(STREET_NAME=row['STREET_NAME'],
                 STREET_NUMBER=row['STREET_NUMBER'],
                 YEAR=row['YEAR'],
                 VALUE=row['VALUE'])

        if d['STREET_NUMBER'].endswith('.0'):
            d['STREET_NUMBER'] = d['STREET_NUMBER'][:-2]

        if d['YEAR'].endswith('.0'):
            d['YEAR'] = d['YEAR'][:-2]

        d_list.append(d)

    y = str(int(d_list[1]['YEAR']))
    fpout = open('../data/property_tax_06_15/latlong_property_tax_'+ str(y) + '.csv', 'w')
    fpout.write('YEAR,VALUE,STREET_NUMBER,STREET_NAME,LATITUDE,LONGITUDE\n')

    random.shuffle(d_list)
    n_lines = float(len(d_list))
    curr_line = 0
    for d in d_list:
        curr_line += 1
        st_num = str(int(d['STREET_NUMBER']))
        st_name = str(d['STREET_NAME'])
        
        if (st_name, st_num) in local_db:
            latitude, longitude = local_db[(st_name, st_num)]
        else:
            print 'querying...'      
            address = st_num + ' ' + st_name + ' Vancouver BC Canada'

            got_it = False
            delay = 1
            while not got_it:
                try:
                    sleep(1)
                    location = geolocator.geocode(address)
                    got_it = True
                except (GeopyError, SSLError) as e:
                    delay *= 2
                    got_it = False
                    print 'try again...'

            latitude = "{:.15f}".format(location.latitude)
            longitude = "{:.15f}".format(location.longitude)
        
        curr_value = str(float(d['VALUE']))

        fpout.write(str(y) + ',' + curr_value + ',' + st_num + ',' + st_name + ',' + latitude + ',' + longitude + '\n')
        print str(100 * curr_line/n_lines) + '%, ' + str(y) + ',' + curr_value + ',' + latitude + ',' + longitude + ', '+ st_num, st_name
        local_db[(st_name, st_num)] = (latitude, longitude)

    fpin.close()
    fpout.close()


def load_local_db():
    for y in xrange(2006, 2016):
        path = '../data/property_tax_06_15/latlong_property_tax_'+ str(y) + '.csv'
        if os.path.isfile(path):
            print 'loading', path
            fp = open(path, 'r')
            for line in fp:
                tokens = line.strip().split(',')
                st_num = tokens[2]
                st_name = tokens[3]
                lat = tokens[4]
                lon = tokens[5]
                if (st_name, st_num) not in local_db:
                    local_db[(st_name, st_num)] = (lat, lon)


if __name__ == '__main__':
    load_local_db()
    for path in sys.argv[1:]:
        main(path)

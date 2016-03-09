__author__ = 'walthermaciel'

from geopy.geocoders import DataBC
from time import sleep
import sys

def main(y):
    geolocator = DataBC()

    print 'starting', y
    fpin = open('../data/property_tax_06_15/property_tax_report_csv' + str(y) + '.csv', 'r')
    fpout = open('../data/property_tax_06_15/clean_property_tax_'+ str(y) + '.csv', 'w')

    i_st_name = -1
    i_st_num = -1
    i_curr_value = -1
    i_pid = -1

    for i, line in enumerate(fpin):
        cols = line.replace(', ', ' ').strip().split(',')

        if i == 0:
            for i_c, c in enumerate(cols):
                if c == 'STREET_NAME':
                    i_st_name = i_c
                elif c == 'TO_CIVIC_NUMBER':
                    i_st_num = i_c
                elif c == 'PID':
                    i_pid = i_c
                elif c == 'CURRENT_LAND_VALUE':
                    i_curr_value = i_c
            fpout.write('YEAR,PID,LAND_VALUE,LAT,LONG\n')

        else:
            # Check if it has PID
            pid = cols[i_pid]
            if pid == '':
                continue

            # Check if it has street name
            st_name = cols[i_st_name]
            if st_name == '':
                continue

            # Check if it has street number
            st_num = cols[i_st_num]
            if st_num == '':
                continue

            # Check if it has current land value
            curr_value = cols[i_curr_value]
            if curr_value == '':
                continue

            address = st_num + ' ' + st_name + ' Vancouver BC Canada'

            found_it = False
            while not found_it:
                try:
                    location = geolocator.geocode(address)
                    sleep(0.5)
                    found_it = True
                except:
                    found_it = False

            latitude = str(location.latitude)
            longitude = str(location.longitude)

            fpout.write(str(y) + ',' + pid + ',' + curr_value + ',' + latitude + ',' + longitude + '\n')
            print str(y) + ',' + pid + ',' + curr_value + ',' + latitude + ',' + longitude + ', '+ st_num, st_name

        fpin.close()
        fpout.close()



if __name__ == '__main__':
    main(sys.argv[1])

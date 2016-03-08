__author__ = 'walthermaciel'
from utilities import utm_to_latlong

def main():
    crime_fp = open('../data/crime_03_15/crime_csv_all_years.csv', 'r')
    clean_fp = open('../data/crime_03_15/crime_latlong.csv', 'w')

    for line in crime_fp:
        cols = line.strip().split(',')
        crime_type, year, month, hundred_block, nhood, aux, utm_x, utm_y = cols

        if utm_x != '0' and utm_y != '0':

            if crime_type != 'TYPE':
                x = float(utm_x)
                y = float(utm_y)
                lat, lon = utm_to_latlong(x, y)
                latitude = str(lat)
                longitude = str(lon)
            else:
                latitude = 'LATITUDE'
                longitude = 'LONGITUDE'

            clean_fp.write(crime_type +','+ year +','+ month +','+ hundred_block +','+ nhood +','+ latitude +','+ longitude +'\n')

    crime_fp.close()
    clean_fp.close()


if __name__ == '__main__':
    main()

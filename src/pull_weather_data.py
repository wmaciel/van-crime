from urllib2 import Request, HTTPError, URLError, urlopen
from datetime import timedelta, date
import csv, os


codenames = {888 : 'VANCOUVER HARBOUR CS', 51357: 'VANCOUVER SEA ISLAND CCG', 889: 'VANCOUVER INT\'L A'}

def daterange(start,end):
    for n in range(int((end-start).days)):
        yield start + timedelta(n)

def dlfile(code, year):

    url = 'http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=csv&stationID=' + str(code) +\
          '&Year=' + str(year) +\
          '&Month=1&Day=1&timeframe=2&submit=Download+Data'
    project_root = '../'
    filename = project_root + 'data/weather/' + codenames[code] + '/' + str(year) + 'data.csv'
    req = Request(url)

    if not os.path.exists('../data/weather/' + codenames[code]):
        os.makedirs('../data/weather/' + codenames[code])

    try:
        f = urlopen(req)
        print 'downloading', year
        local_file = open(filename, 'wb')
        wr = csv.writer(local_file)

        for idx, line in enumerate(f):
            if idx > 24:
                row_val = line.strip().split(',')
                row_val = [element.replace('"', '') for element in row_val]
                wr.writerow(row_val)

        local_file.close()

    except HTTPError, e:
        print 'HTTP Error:', e.code, url
    except URLError, e:
        print 'URLError:', e.reason, url


def main():

    for code_val in [888, 889, 51357]:
        for year_val in xrange(2006, 2016, 1):
            dlfile(code_val, year_val)


if __name__ == "__main__":
    main()
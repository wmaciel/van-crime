'''
Created on Mar 2, 2016

@author: loongchan
'''
# from pykml import parser
# from pykml.parser import Schema
import utm
from os import path

'''
Tool to convert from UTM to lat/long
'''
def utm_to_latlong(easting, northing, zone_number = 10, zone_letter = 'U'):
    try:
        return utm.to_latlon(easting, northing, zone_number, zone_letter)
    except:
        print "You might need to install utm.. 'pip install utm'"
        

def latlong_to_utm(lat, long):
    try:
        return utm.from_latlon(lat, long)
    except:
        print "You might need to install utm.. 'pip install utm'"
        
'''
def load_kml(filename):
    with open(filename) as fh:
        schema_gx = Schema("kml22gx.xsd")
        doc = parser.parse(fh)
        
        if (schema_gx.validate(doc)):
            return doc.getroot()
        else:
            print "Invalid kml format for file: "+str(filename)
            return None
'''
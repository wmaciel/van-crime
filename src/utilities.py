'''
Created on Mar 2, 2016

@author: loongchan
'''
from pykml import parser
from pykml.parser import Schema
from geopy.distance import vincenty
import utm, os.path, csv
#from nis import cat

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
        
def load_kml_file(filename, schema_type = "kml22gx.xsd"):
    with open(filename) as fh:
        schema_gx = Schema(schema_type)
        doc = parser.parse(fh)
        
        if (schema_gx.validate(doc)):
            return doc.getroot()
        else:
            print "Invalid kml format for file: "+str(filename)
            return None

def load_kml_string(kml_string, schema_type = "kml22gx.xsd"):
    schema_gx = Schema(schema_type)
    doc = parser.fromstring(kml_string, schema_gx)
    
    if (schema_gx.validate(doc)):
        return doc
    else:
        print "Invalid kml format for string passed in"
        return None
    
    
def kml_to_csv(kml_file, use_headers=True, output_filename = 'output.csv'):
    #if file, then load it, else it's a string
    root = None
    if os.path.isfile(kml_file):
        root =load_kml_file(kml_file)
    else:
        root = load_kml_string(kml_file)
    
    # now we start parsing the xml... isn't there a better way???
    with open(output_filename, 'wb') as fh:
        csv_out = csv.writer(fh)
        
        #get headers if we want it
        if use_headers:
            header_line = list();
            for child in root.Document.Folder.Placemark.ExtendedData.iter():
                if 'name' in dict(child.attrib):
                    header_line.append(child.attrib['name'])
            header_line.append('LAT')
            header_line.append('LONG')
            csv_out.writerow(header_line)
        
        #we save all data AND location via lat/long
        for child in root.Document.Folder.iter():
            if 'Placemark' in child.tag:
                line_str = list()
                for gchild in child.iter():
                    if 'ExtendedData' in gchild.tag:
                        for ggchild in child.iter():
                            if 'SimpleData' in ggchild.tag:
                                line_str.append(ggchild.text)
                    if 'Point' in gchild.tag:
                        coords_split = str(gchild.coordinates).split(',')
                        line_str.append(coords_split[1])
                        line_str.append(coords_split[0])
                        
                                
                csv_out.writerow(line_str)

def number_of_graffiti_points(latitude, longitude, radius1=50, radius2=100, graffiti_fh=None):
    graffiti_file = '../data/graffiti/graffiti.csv'
    
    # check if graffiti_fh is NOT empty
    open_myself = False
    if graffiti_fh is None:
        graffiti_fh = open(graffiti_file, 'rb')
        open_myself = True
        
    graffiti_fh.seek(0)
    graffiti_reader = csv.DictReader(graffiti_fh)
    
    # yeah, we check the point against all 8k+ rows..yeah, yeah....
    count1 = 0
    count2 = 0
    for row in graffiti_reader:        
        latlong_diff = vincenty((latitude, longitude), (row['LAT'],row['LONG']))

        #set counts based on radius1 and radius2
        if latlong_diff.m < radius1:
            count1 = count1 + int(row['COUNT'])
        
        if latlong_diff.m < radius2:
            count2 = count2 + int(row['COUNT'])
                    
    #now we got the counts, we need to clean up and return
    if open_myself:
        graffiti_fh.close()
        
    return (count1, count2)

# takes lat/long and returns distance from nearest (Adult, Men, Women/Families, Youth)
def number_of_homeless_shelters_at(latitude, longitude, homeless_fh=None):
    homeless_file = '../data/homeless_shelters/doc.csv'
    
    # check if graffiti_fh is NOT empty
    open_myself = False
    if homeless_fh is None:
        homeless_fh = open(homeless_file, 'rb')
        open_myself = True
        
    homeless_fh.seek(0)
    homeless_reader = csv.DictReader(homeless_fh)
    
    # yeah, we check the point against all 8k+ rows..yeah, yeah....
    keys = ['adults', 'men', 'women/families', 'youth']
    retval = dict((x, float('Inf')) for x in keys)
    for row in homeless_reader:        
        latlong_diff = vincenty((latitude, longitude), (row['LAT'],row['LONG']))
        
        #we need to consider the "category" of which there is 4.
        cat = row['CATEGORY'].split(' ')[0].lower()
        if retval[cat] > latlong_diff.m:
            retval[cat] = latlong_diff.m
    
    # now we get the tuple from dict in order, since for feature vector we care about that kind of stuff
    final_retval = tuple()
    for c in keys:
        final_retval = final_retval + (retval[c],)
        
    #now we got the counts, we need to clean up and return
    if open_myself:
        homeless_fh.close()
        
    return final_retval
    

def number_of_street_lights_at(latitude, longitude, light_fh=None, radius1=50):
    light_file = '../data/street_lightings/street_lighting_poles.csv'
    
    # check if graffiti_fh is NOT empty
    open_myself = False
    if light_fh is None:
        light_fh = open(light_file, 'rb')
        open_myself = True
        
    light_fh.seek(0)
    light_reader = csv.DictReader(light_fh)
    
    # yeah, we check the point against all 8k+ rows..yeah, yeah....
    count1 = 0
    for row in light_reader:        
        latlong_diff = vincenty((latitude, longitude), (row['LAT'],row['LONG']))
        
        #set counts based on radius1
        if latlong_diff.m < radius1:
            count1 = count1 + 1
        
    #now we got the counts, we need to clean up and return
    if open_myself:
        light_fh.close()
        
    return (count1,)
    





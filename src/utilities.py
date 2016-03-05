'''
Created on Mar 2, 2016

@author: loongchan
'''
from pykml import parser
from pykml.parser import Schema
import utm, os.path, csv

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










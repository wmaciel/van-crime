'''
Created on Mar 4, 2016

@author: loongchan
'''
import utilities
import re

def homeless_kml_to_csv(kml_filename, use_headers=True, output_filename = 'doc.csv'):
    # we need to read it to string cause parser complains, so we need to clean it a bit first
    with open(kml_filename, 'r') as myfile:
        dataz=myfile.read().replace('\n', '')
    
    # we need to clean via regex 
    dataz = re.sub(r"<gx:labelVisibility>\d+</gx:labelVisibility>", "", dataz)

    #ok, just call magic function
    utilities.kml_to_csv(dataz, use_headers=True, output_filename='doc.csv')


def graffiti_kml_to_csv(kml_filename):
    #ok, just call magic function
    utilities.kml_to_csv(kml_filename, use_headers=True, output_filename='graffiti.csv')

homeless_kml_to_csv('../data/homeless_shelters/doc.kml')     
graffiti_kml_to_csv('../data/graffiti/graffiti.kml')
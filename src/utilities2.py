'''
Created by:
Juan Sarria
March 15, 2016
'''
import pandas as pd, numpy as np, timeit
from geopy.distance import vincenty


project_root = '../'

def main():
    #test values
    lat = 49.28334
    lon = -123.113
    '''
    prop_df = pd.read_csv(project_root + 'data/property_tax_06_15/latlong_property_tax_' + str(2006) + '.csv')
    print avg_closest_properties(lat,lon,prop_df=prop_df)

    sky_df = pd.read_csv(project_root + 'data/skytrain_stations/rapid_transit_stations.csv')
    print closest_skytrain(lat,lon)

    crime_df = pd.read_csv(project_root+'/data/crime_03_15/crime_latlong.csv')
    neighbourhoods = crime_df['NEIGHBOURHOOD'].unique().tolist()
    print len(neighbourhoods)
    print one_hot_encoding(neighbourhoods[2],neighbourhoods)
    '''
    a = number_graffiti(lat,lon)
    print type(a[0])

def avg_closest_properties(lat, lon,year = None, prop_df = None, range_val = 0.0001):

    try:
        if year is not None:
            property_file = project_root + 'data/property_tax_06_15/latlong_property_tax_' + str(year) + '.csv'
            if prop_df is None: prop_df = pd.read_csv(property_file)

        # Keep a copy of original df
        temp_df = prop_df

        # Narrow down options to minimize unnecessary calculations
        prop_df = prop_df[prop_df['LATITUDE']< lat+range_val]
        prop_df = prop_df[prop_df['LATITUDE']> lat-range_val]
        prop_df = prop_df[prop_df['LONGITUDE']< lon+range_val]
        prop_df = prop_df[prop_df['LONGITUDE']> lon-range_val]

        # If not enough values, start again with a bigger range
        if prop_df.count()['VALUE'] < 10:
            return avg_closest_properties(lat,lon,prop_df=temp_df,range_val=range_val*10)


        # Apply vincenty in the remaining rows
        prop_df['DIST_DIF'] =  prop_df.apply(lambda row: vincenty((lat,lon),(row['LATITUDE'],row['LONGITUDE'])).m,axis=1)

        # Find the top 10 and top 5 closest properties
        ten_min_df = prop_df[['VALUE','DIST_DIF']].nsmallest(10,'DIST_DIF')
        five_min_df = ten_min_df.nsmallest(5,'DIST_DIF')

        # Return average property value for he top 5 and 10
        return [five_min_df['VALUE'].mean(),ten_min_df['VALUE'].mean()]

    except:
        print "Error in avg_closest_properties"


def closest_skytrain(lat,lon, sky_df = None):

    skytrain_file = project_root + 'data/skytrain_stations/rapid_transit_stations.csv'
    if sky_df is None: sky_df = pd.read_csv(skytrain_file)

    vector = [0]*(sky_df.count()['STATION']+1)

    # Find closest skytrain station
    sky_df['DIST_DIF'] = sky_df.apply(lambda row: vincenty((lat,lon),(row['LAT'],row['LONG'])).m,axis=1)
    min_df = sky_df.nsmallest(1,'DIST_DIF')

    vector[list(min_df.index)[0]] = 1
    vector[-1] = min_df.iloc[0]['DIST_DIF']

    # returns on-hot encoded vector with distance at the end
    return vector

def one_hot_encoding(label, list_of_labels):

    vector = [0]*len(list_of_labels)
    vector[list_of_labels.index(label)] = 1
    return vector

def number_graffiti(lat,lon, graf_df = None, radius1 = 50, radius2 = 100):

    graffiti_file = project_root + 'data/graffiti/graffiti.csv'
    if graf_df is None: graf_df = pd.read_csv(graffiti_file)

    # Narrow down options
    graf_df = graf_df[graf_df['LAT'] < lat+.001]
    graf_df = graf_df[graf_df['LAT'] > lat-.001]
    graf_df = graf_df[graf_df['LONG'] < lon+.001]
    graf_df = graf_df[graf_df['LONG'] < lon+.001]

    if graf_df['LAT'].count() == 0: return [0,0]

    # Apply vincenty for remaining rows
    graf_df['DIST_DIF'] = graf_df.apply(lambda row: vincenty((lat,lon),(row['LAT'],row['LONG'])).m,axis=1)

    count_2 = graf_df[graf_df['DIST_DIF'] <= radius2]
    count_1 = count_2[count_2['DIST_DIF'] <= radius1]

    return [count_1['COUNT'].sum(), count_2['COUNT'].sum()]

def number_street_lights(lat,lon,light_df = None, radius = 50):
    light_file = project_root + 'data/street_lightings/street_lighting_poles.csv'
    if light_df is None: light_df = pd.read_csv(light_file)
    
    # Narrow down options
    light_df = light_df[light_df['LAT'] < lat+.001]
    light_df = light_df[light_df['LAT'] > lat-.001]
    light_df = light_df[light_df['LONG'] < lon+.001]
    light_df = light_df[light_df['LONG'] < lon+.001]

    if light_df['LAT'].count() == 0 : return 0

    # Apply vincenty and find number of lights within radius
    light_df['DIST_DIF'] = light_df.apply(lambda row: vincenty((lat,lon),(row['LAT'],row['LONG'])).m,axis=1)
    min_lights = light_df[light_df['DIST_DIF'] < radius]

    return  min_lights['DIST_DIF'].count()




    


if __name__ == "__main__":
    main()







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
    prop_df = pd.read_csv(project_root + 'data/property_tax_06_15/latlong_property_tax_' + str(2009) + '.csv')
    print avg_closest_properties(2009,lat,lon,prop_df=prop_df)

def avg_closest_properties(year, lat, long, prop_df = None, range_val = 0.0001):
    property_file = project_root + 'data/property_tax_06_15/latlong_property_tax_' + str(year) + '.csv'

    if prop_df is None: prop_df = pd.read_csv(property_file)

    # Keep a copy of original df
    temp_df = prop_df

    # Narrow down options to minimize unnecessary calculations
    prop_df = prop_df[prop_df['LATITUDE']< lat+range_val]
    prop_df = prop_df[prop_df['LATITUDE']> lat-range_val]
    prop_df = prop_df[prop_df['LONGITUDE']< long+range_val]
    prop_df = prop_df[prop_df['LONGITUDE']> long-range_val]

    # If not enough values, start again with a bigger range
    if prop_df.count()['VALUE'] < 10:
        return avg_closest_properties(year,lat,long,prop_df=temp_df,range_val=range_val*10)


    prop_df['DIST_DIF'] =  prop_df.apply(lambda row: vincenty((lat,long),(row['LATITUDE'],row['LONGITUDE'])).km,axis=1)

    ten_min_df = prop_df[['VALUE','DIST_DIF']].nsmallest(10,'DIST_DIF')
    five_min_df = ten_min_df.nsmallest(5,'DIST_DIF')

    return (five_min_df['VALUE'].mean(),ten_min_df['VALUE'].mean())
    


if __name__ == "__main__":
    main()







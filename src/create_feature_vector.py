'''
Created by:
Juan Sarria
March 17, 2016
'''
import pandas as pd, timeit as tm, pickle as pk, csv
from utilities2 import one_hot_encoding, number_graffiti, avg_closest_properties, closest_skytrain, number_street_lights
from utilities import number_of_homeless_shelters_at

project_root = '../'
TEST_VAL = True

def main():
    print 'Reading in crime_data...'
    time1 = tm.default_timer()
    crime_data = pd.read_csv(project_root+'/data/crime_03_15/crime_latlong.csv')
    print 'Finished'
    print 'Time taken:', tm.default_timer()-time1, ' seconds\n'
##################################################################################

    print 'Trimming unnecessary data...'
    time1 = tm.default_timer()
    crime_data = crime_data[crime_data['YEAR'] >= 2006]
    crime_data = crime_data[crime_data['YEAR'] <= 2015]
    crime_data = crime_data[pd.notnull(crime_data['NEIGHBOURHOOD'])]
    crime_data = crime_data.drop('HUNDRED_BLOCK', axis=1)
    print 'Finished'
    print 'Time taken:', tm.default_timer()-time1, ' seconds\n'
##################################################################################

    if TEST_VAL:
        print 'Taking subset of crime data (1000 row sample)...'
        crime_data = crime_data.sample(1000)
        print ''
##################################################################################

    print 'Creating labels...'
    time1 = tm.default_timer()
    labels = crime_data['TYPE']
    crime_data = crime_data.drop('TYPE', axis=1)
    type_vals = labels.unique().tolist()
    labels = labels.apply(lambda x: pd.Series(one_hot_encoding(x,type_vals),index=type_vals))
    labels = pd.concat([crime_data['YEAR'], labels], axis=1)
    print 'Finished'
    print 'Time taken:', tm.default_timer()-time1, ' seconds\n'
##################################################################################

    print 'One-hot encoding neighbourhoods...'
    time1 = tm.default_timer()
    neighbourhoods = crime_data['NEIGHBOURHOOD']
    crime_data = crime_data.drop('NEIGHBOURHOOD', axis=1)
    n_types = neighbourhoods.unique().tolist()
    n_index = [('n_'+x.replace(' ','_')).upper() for x in n_types]
    neighbourhoods = neighbourhoods.apply(lambda x: pd.Series(one_hot_encoding(x,n_types),index=n_index))
    print 'Finished'
    print 'Time taken:', tm.default_timer()-time1, ' seconds\n'
##################################################################################

    print 'Getting graffiti count...'
    time1 = tm.default_timer()
    graf_df = pd.read_csv(project_root+'data/graffiti/graffiti.csv')
    graffiti = crime_data[['LATITUDE', 'LONGITUDE']]
    graffiti = graffiti.apply(lambda row: pd.Series(number_graffiti(row['LATITUDE'],row['LONGITUDE'],graf_df),
                                                    index=['G_50M', 'G_100M']), axis=1)
    print 'Finished'
    print 'Time taken:', tm.default_timer()-time1, ' seconds\n'
##################################################################################

    print 'Getting closest homeless shelters...'
    time1 = tm.default_timer()
    h_fh = open(project_root+'data/homeless_shelters/doc.csv')
    homeless = crime_data[['LATITUDE','LONGITUDE']]
    homeless = homeless.apply(lambda row: pd.Series(number_of_homeless_shelters_at(row['LATITUDE'],row['LONGITUDE'],
                                                                                   homeless_fh=h_fh),
                                                    ['H_ADULT','H_MEN','H_WOMEN_FAM','H_YOUTH']),axis=1)
    print 'Finished'
    print 'Time taken:', (tm.default_timer()-time1), ' seconds\n'
##################################################################################

    print 'Calculating average property values...'
    time1 = tm.default_timer()
    prop_dfs = dict((x, pd.read_csv(project_root+'data/property_tax_06_15/latlong_property_tax_' + str(x) + '.csv'))
                     for x in xrange(2006,2016,1))
    prop_values = crime_data[['YEAR','LATITUDE','LONGITUDE']]
    prop_values = prop_values.apply(lambda  row: pd.Series(avg_closest_properties(row['LATITUDE'],
                                                                                  row['LONGITUDE'],
                                                                                  prop_df=prop_dfs[int(row['YEAR'])]),
                                                          ['P_AVG5', 'P_AVG10']), axis=1)
    print 'Finished'
    print 'Time taken:', (tm.default_timer()-time1),'seconds\n'
##################################################################################

    print 'Finding closest skytrain...'
    time1 = tm.default_timer()
    sky_df = pd.read_csv(project_root + 'data/skytrain_stations/rapid_transit_stations.csv')
    s_index = ['S_'+x.replace(' ','_') for x in sky_df['STATION'].tolist()] + ['S_DISTANCE']
    sky = crime_data[['LATITUDE','LONGITUDE']]
    sky = sky.apply(lambda row: pd.Series(closest_skytrain(row['LATITUDE'],row['LONGITUDE'],sky_df), index=s_index),
                    axis=1)
    print 'Finished'
    print 'Time taken:', (tm.default_timer()-time1),'seconds\n'
##################################################################################

    print 'Getting street light count...'
    time1 = tm.default_timer()
    light_df = pd.read_csv(project_root + 'data/street_lightings/street_lighting_poles.csv')
    lights = crime_data[['LATITUDE','LONGITUDE']]
    lights = lights.apply(lambda row: pd.Series(number_street_lights(row['LATITUDE'], row['LONGITUDE'], light_df),
                                                index=['SL_50M']),axis=1)
    print 'Finished'
    print 'Time taken:', (tm.default_timer()-time1),'seconds\n'
##################################################################################

    print 'Getting monthly weather information...'
    time1 = tm.default_timer()
    weather_df = pd.read_csv(project_root + 'data/weather/VANCOUVER SEA ISLAND CCG/summarydata.csv')

    weather = crime_data[['YEAR', 'MONTH']]
    weather = weather.reset_index().merge(weather_df).set_index('index')

    weather = weather.drop('YEAR',axis=1).drop('MONTH',axis=1)

    print 'Finished'
    print 'Time taken:', (tm.default_timer()-time1),'seconds\n'

##################################################################################

    print 'Concatenating information...'

    feature_vectors = pd.concat([crime_data, neighbourhoods, graffiti, homeless, prop_values, sky, lights, weather],
                                axis=1)

##################################################################################

    print 'Outputting to csv and pickle...'

    output_folder = project_root + 'data/clean_data/'
    if TEST_VAL: output_folder += 'subset/'

    train_vectors = feature_vectors[feature_vectors['YEAR']< 2015]
    test_vectors  = feature_vectors[feature_vectors['YEAR'] == 2015]

    train_labels = labels[labels['YEAR'] < 2015].drop('YEAR',axis=1)
    test_labels  = labels[labels['YEAR'] == 2015].drop('YEAR',axis=1)

    train_vectors.to_csv(output_folder+'train_vectors.csv', sep=',', encoding='utf-8')
    train_vectors.to_pickle(output_folder+'train_vectors.pickle')
    
    test_vectors.to_csv(output_folder+'test_feature_vectors.csv', sep=',', encoding='utf-8')
    test_vectors.to_pickle(output_folder+'test_feature_vectors.pickle')
    
    train_labels.to_csv(output_folder+'train_labels.csv', sep=',', encoding='utf-8')
    train_labels.to_pickle(output_folder+'train_labels.pickle')
    
    test_labels.to_csv(output_folder+'test_labels.csv', sep=',', encoding='utf-8')
    test_labels.to_pickle(output_folder+'test_labels.pickle')
    




















if __name__ == "__main__":
    main()
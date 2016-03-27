'''
Created by:
Juan Sarria
March 17, 2016
'''
import pandas as pd, timeit as tm, pickle as pk, csv, sys
from utilities2 import one_hot_encoding, number_graffiti, avg_closest_properties, closest_skytrain, number_street_lights
from utilities import number_of_homeless_shelters_at

PROJECT_ROOT = '../'
TEST_VAL = True
if TEST_VAL:
    SPLIT_SIZE = 100
else:
    SPLIT_SIZE = 1000


# complete data on crimes
MAIN_DATA = pd.read_csv(PROJECT_ROOT+'/data/crime_03_15/crime_latlong.csv')
# graffiti dataframe
GRAF_DF = pd.read_csv(PROJECT_ROOT+'data/graffiti/graffiti.csv')
# property value dataframes
PROP_DFS = dict((x, pd.read_csv(PROJECT_ROOT+'data/property_tax_06_15/latlong_property_tax_' + str(x) + '.csv'))
                     for x in xrange(2006,2016,1))
# weather dataframe
WEATHER_DF = pd.read_csv(PROJECT_ROOT + 'data/weather/VANCOUVER SEA ISLAND CCG/summarydata.csv')


def create_labels(crime_data, output_folder = None, p_ext = ''):
    print 'Creating labels and outputting to csv and pickle...',
    time1 = tm.default_timer()
    type_vals = MAIN_DATA['TYPE'].unique().tolist()
    labels = crime_data['TYPE']
    labels = labels.apply(lambda x: pd.Series(one_hot_encoding(x,type_vals),index=type_vals))
    labels = pd.concat([crime_data['YEAR'], labels], axis=1)

    train_labels = labels[labels['YEAR'] < 2015]
    test_labels = labels[labels['YEAR'] == 2015]
    if output_folder is not None:
        train_labels.to_csv(output_folder+'csv/train_labels' + p_ext + '.csv', sep=',', encoding='utf-8')
        train_labels.to_pickle(output_folder+'pickle/train_labels' + p_ext + '.pickle')
        test_labels.to_csv(output_folder+'csv/test_labels' + p_ext + '.csv', sep=',', encoding='utf-8')
        test_labels.to_pickle(output_folder+'pickle/test_labels' + p_ext + '.pickle')
    print 'Finished'
    print 'Time taken:', tm.default_timer()-time1, ' seconds\n'

def create_vectors(row = None, part = None, total_parts = None, output_folder = None):

    def get_neighbourhoods():
        print 'Reading in additional data and setting variables...'
        time1 = tm.default_timer()
        # list of neighbourhoods
        n_types = MAIN_DATA['NEIGHBOURHOOD']
        n_types = n_types[pd.notnull(n_types)].unique().tolist()
        n_index = [('n_'+x.replace(' ','_')).upper() for x in n_types]
        print 'Finished'
        print 'Time taken:', tm.default_timer()-time1, ' seconds\n'

        return n_types, n_index

    def trim_data(crime_data, part, total_parts):
        print 'Trimming unnecessary data...',
        time1 = tm.default_timer()
        crime_data = crime_data[crime_data['YEAR'] >= 2006]
        crime_data = crime_data[crime_data['YEAR'] <= 2015]
        crime_data = crime_data[pd.notnull(crime_data['NEIGHBOURHOOD'])]
        crime_data = crime_data.drop('HUNDRED_BLOCK', axis=1)
        crime_data = crime_data.sort_index()


        if TEST_VAL:
            print 'Taking subset of crime data (1000 row sample)...',
            crime_data = crime_data.head(1005)
            SPLIT_SIZE = 100

        if part is not None and total_parts is not None:
            start_index = int(1.0*(part-1)/total_parts*crime_data['YEAR'].count())
            end_index = int(1.0*part/total_parts*crime_data['YEAR'].count())

            if part == total_parts:
                end_index = crime_data['YEAR'].count()

            crime_data = crime_data[start_index:end_index]

            print 'Start index, end index, size:',start_index,end_index, crime_data['YEAR'].count()

        print 'Finished'
        print 'Time taken:', tm.default_timer()-time1, ' seconds\n'
        return crime_data

    def split_frames(crime_data):
        print 'Splitting dataframe...',
        time1 = tm.default_timer()
        crime_dfs = []
        num_splits = int(crime_data['YEAR'].count()/SPLIT_SIZE)
        for i in xrange(0,num_splits,1):
            crime_dfs.append(crime_data[i*SPLIT_SIZE:(i+1)*SPLIT_SIZE])
        if crime_data['YEAR'].count() > SPLIT_SIZE*num_splits:
            crime_dfs.append(crime_data[SPLIT_SIZE*num_splits:])
            num_splits+=1
        print 'Finished'
        print 'Time taken:', tm.default_timer()-time1, ' seconds\n'

        return crime_dfs

    def calculate_vectors(crime_df):

                print 'One-hot encoding neighbourhoods...',
                neighbourhoods = crime_df['NEIGHBOURHOOD']
                crime_df = crime_df.drop('NEIGHBOURHOOD', axis=1)
                neighbourhoods = neighbourhoods.apply(lambda x: pd.Series(one_hot_encoding(x,n_types),index=n_index))

            ##################################################################################
                print 'Getting graffiti count...',

                graffiti = crime_df[['LATITUDE', 'LONGITUDE']]
                graffiti = graffiti.apply(lambda row: pd.Series(number_graffiti(row['LATITUDE'],row['LONGITUDE'],
                                                                                GRAF_DF),
                                                                index=['G_50M', 'G_100M']), axis=1)

            ##################################################################################

                print 'Getting closest homeless shelters...',
                homeless = crime_df[['LATITUDE','LONGITUDE']]
                homeless = homeless.apply(lambda row: pd.Series(number_of_homeless_shelters_at(row['LATITUDE'],
                                                                                               row['LONGITUDE'],
                                                                                               homeless_fh=h_fh),
                                                                ['H_ADULT','H_MEN','H_WOMEN_FAM','H_YOUTH']),axis=1)

            ##################################################################################

                print 'Calculating average property values...',
                prop_values = crime_df[['YEAR','LATITUDE','LONGITUDE']]
                prop_values = prop_values.apply(lambda  row: pd.Series(avg_closest_properties(row['LATITUDE'],
                                                                                              row['LONGITUDE'],
                                                                                              prop_df=PROP_DFS[int(row['YEAR'])]),
                                                                      ['P_AVG5', 'P_AVG10']), axis=1)

            ##################################################################################

                print 'Finding closest skytrain...',
                sky_df = pd.read_csv(PROJECT_ROOT + 'data/skytrain_stations/rapid_transit_stations.csv')
                s_index = ['S_'+x.replace(' ','_') for x in sky_df['STATION'].tolist()] + ['S_DISTANCE']
                sky = crime_df[['LATITUDE','LONGITUDE']]
                sky = sky.apply(lambda row: pd.Series(closest_skytrain(row['LATITUDE'],row['LONGITUDE'],sky_df),
                                                      index=s_index),axis=1)

            ##################################################################################

                print 'Getting street light count...',
                light_df = pd.read_csv(PROJECT_ROOT + 'data/street_lightings/street_lighting_poles.csv')
                lights = crime_df[['LATITUDE','LONGITUDE']]
                lights = lights.apply(lambda row: pd.Series(number_street_lights(row['LATITUDE'], row['LONGITUDE'],
                                                                                 light_df),index=['SL_50M']),axis=1)
            ##################################################################################

                print 'Getting monthly weather information...',

                weather = crime_df[['YEAR', 'MONTH']]
                weather = weather.reset_index().merge(WEATHER_DF).set_index('index')
                weather = weather.drop('YEAR',axis=1).drop('MONTH',axis=1)

                return pd.concat([crime_df,neighbourhoods,graffiti,homeless,prop_values,sky,lights,weather], axis=1)

##################################################################################
    print 'Setting crime_data...'
    if row is None:
        crime_data = MAIN_DATA
    else:
        crime_data = row

 ##################################################################################

    # Neighbourhood values
    n_types, n_index = get_neighbourhoods()
    # Homeless shelter file
    h_fh = open(PROJECT_ROOT+'data/homeless_shelters/doc.csv')

 ##################################################################################

    # Output Settings
    if output_folder is None: output_folder = PROJECT_ROOT + 'data/clean_data/'
    p_ext = ''
    if TEST_VAL: output_folder += 'subset/'
    if part is not None: p_ext = '_'+str(part)

    if row is None:
        train_vect_csv = open(output_folder+'csv/train_vectors' + p_ext + '.csv', mode='a')
        test_vect_csv = open(output_folder+'csv/test_vectors' + p_ext + '.csv', mode='a')

 ##################################################################################

    if row is None: crime_data = trim_data(crime_data,part,total_parts)

 ##################################################################################

    if row is None:
        crime_dfs = split_frames(crime_data)
    else:
        crime_dfs = [crime_data]

 ##################################################################################

    if row is None:
        create_labels(crime_data, output_folder, p_ext)

 ##################################################################################

    # Additional variables
    count = 0
    max_count = crime_data['YEAR'].count()
    feature_vectors = crime_data
 ##################################################################################


    for idx, crime_df in enumerate(crime_dfs):
        time1 = tm.default_timer()
        count += crime_df['YEAR'].count()
        print 'Finding ' + str(count) + '/' + str(max_count) + ' vectors'

        sub_f = calculate_vectors(crime_df)
        header = False

        if idx == 0:
            feature_vectors = sub_f
            header = True
        else:
            feature_vectors = pd.concat([feature_vectors,sub_f], axis=0)


        # Print to csv if not in single-row mode
        if row is None:
            sub_f[sub_f['YEAR'] < 2015].to_csv(train_vect_csv,sep=',',header=header,encoding='utf-8')
            sub_f[sub_f['YEAR'] == 2015].to_csv(test_vect_csv,sep=',',header=header,encoding='utf-8')

        print 'Time taken =', tm.default_timer() - time1, 'seconds\n'


 ##################################################################################

    # Close homeless shelter file
    h_fh.close()

    # Create a pickle if not in single-row mode
    if row is None:
        print 'Outputting vectors to pickle file and closing open csv files...'
        train_vectors = feature_vectors[feature_vectors['YEAR']< 2015]
        test_vectors  = feature_vectors[feature_vectors['YEAR'] == 2015]

        train_vectors.to_pickle(output_folder+'pickle/train_vectors' + p_ext + '.pickle')
        test_vectors.to_pickle(output_folder+'pickle/test_vectors' + p_ext + '.pickle')

        train_vect_csv.close()
        test_vect_csv.close()
    else:
        return feature_vectors

def main():
    part = None
    total_parts = None
    if len(sys.argv) == 3:
        part = int(sys.argv[1])
        total_parts = int(sys.argv[2])
    create_vectors(part=part, total_parts=total_parts)


if __name__ == "__main__":
    main()
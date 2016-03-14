import csv, pandas as pd, numpy as np

def main(pr, fn):

    dfs = []

    for folder_name in fn:

        for i in xrange(2006,2016,1):
            df = pd.read_csv(pr+'data/weather/'+ folder_name + '/' + str(i)  +'data.csv')
            df = df.loc[:,
                 ['Year', 'Month', 'Day', 'Max Temp (\xb0C)', 'Min Temp (\xb0C)', 'Mean Temp (\xb0C)', 'Total Precip (mm)']]
            dfs.append(df)

        weather_data = pd.concat(dfs)
        weather_data = weather_data.groupby(['Year','Month']).agg({'Max Temp (\xb0C)': np.mean,
                                                                   'Min Temp (\xb0C)': np.mean,
                                                                   'Mean Temp (\xb0C)': np.mean,
                                                                   'Total Precip (mm)': np.sum})

        print weather_data
        weather_data.to_csv(pr+'data/weather/' + folder_name + '/summarydata.csv')

if __name__ == "__main__":
    project_root = '../'
    folder_names = ['VANCOUVER INT\'L A', 'VANCOUVER HARBOUR CS', 'VANCOUVER SEA ISLAND CCG' ]
    main( project_root, folder_names)
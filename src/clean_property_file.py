__author__ = 'walthermaciel'

import pandas as pd
import numpy as np

def load_csv(path):
    # Load
    print 'Loading', path
    df = pd.read_csv(path)

    # Remove unwanted columns
    print 'Dropping unwanted columns'
    df = df[['PID', 'TAX_ASSESSMENT_YEAR', 'CURRENT_LAND_VALUE', 'STREET_NAME', 'TO_CIVIC_NUMBER']]
    df.columns = ['PID', 'YEAR', 'VALUE', 'STREET_NAME', 'STREET_NUMBER']

    # Remove unwanted rows
    print 'Removing null rows'
    df.replace('', np.nan, inplace=True)
    df.dropna(inplace=True)

    # Compute average value for each property
    print 'Computing average value for same address properties'
    g_df = df.groupby(['STREET_NAME', 'STREET_NUMBER']).mean()
    df = g_df.reset_index()

    return df

def main():
    for y in xrange(2006, 2016):
        print y
        path_in = '../data/property_tax_06_15/property_tax_report_csv' + str(y) + '.csv'
        df = load_csv(path_in)
        path_out = '../data/property_tax_06_15/avg_property_tax_'+ str(y) + '.csv'
        print 'Saving', path_out
        df.to_csv(path_or_buf=path_out, index=False)
        print '\n'

if __name__ == '__main__':
    main()

'''
Created by:
Juan Sarria
March 28, 2016
'''
import pandas as pd

PROJECT_ROOT = '../'
DATA_FOLDER = PROJECT_ROOT+'data/clean_data/'


def compress_vectors(train=True):
    ext = 'train'
    if train == False: ext = 'test'

    vect = pd.read_csv(DATA_FOLDER+ ext +'_vectors.csv', index_col='Unnamed: 0').drop('TYPE',axis=1)
    labl = pd.read_csv(DATA_FOLDER+ ext +'_labels.csv', index_col='Unnamed: 0').drop('YEAR',axis=1)

    data = vect.join(labl,how='inner')
    data = data.groupby(list(vect.columns.values)).sum().reset_index()

    data[list(vect.columns.values)].to_csv(DATA_FOLDER + 'sum/' + ext +'_vectors.csv')
    data[list(labl.columns.values)].to_csv(DATA_FOLDER + 'sum/' + ext +'_labels.csv')


def main():
    compress_vectors()
    compress_vectors(False)


if __name__ == "__main__":
    main()
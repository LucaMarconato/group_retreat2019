import os
import pickle

import pandas as pd

try:
    merged = pickle.load(open("merged.pickle", "rb"))
except (OSError, IOError) as e:
    young_methylation_path = 'MethylationData/Imputed/UD/'
    files = os.listdir(young_methylation_path)
    merged = pd.DataFrame(columns=['start_position'])

    cell_number = 0
    for file in files:
        full_file_path = os.path.join(young_methylation_path, file)
        df = pd.read_csv(full_file_path, sep='\t', header=0)
        df.drop(df.columns[list([0, 2])], axis=1, inplace=True)
        df.columns = ['start_position', 'methylation_state']
        merged = pd.merge(df, merged, how='outer', on='start_position')
        merged.rename(columns={'methylation_state': f'file'}, inplace=True)
    pickle.dump(merged, open("merged.pickle", "wb"))
    print('done')


def print_full(x):
    pd.set_option('display.max_rows', len(x))
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 2000)
    pd.set_option('display.float_format', '{:20,.2f}'.format)
    pd.set_option('display.max_colwidth', -1)
    print(x)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')
    pd.reset_option('display.width')
    pd.reset_option('display.float_format')
    pd.reset_option('display.max_colwidth')

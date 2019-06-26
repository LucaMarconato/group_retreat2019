import os
import pickle
import progressbar

import pandas as pd

def load_methylation_data(folder_path: str) -> pd.DataFrame:
    pickle_path = folder_path.replace('/', '_') + '.pickle'
    try:
        print('loading pickle... ', end='')
        merged = pickle.load(open(pickle_path, "rb"))
        print('done')
    except (OSError, IOError) as e:
        files = os.listdir(folder_path)
        merged = pd.DataFrame(columns=['start_position'])

        print('merging methylation files')
        bar = progressbar.ProgressBar(maxval=len(files),
                                      widgets=[progressbar.Bar('=', '[', ']'),
                                               ' ', progressbar.Percentage()])
        bar.start()
        i = 1
        unique_positions = set()
        for file in files:
            full_file_path = os.path.join(folder_path, file)
            df = pd.read_csv(full_file_path, sep='\t', header=0)
            df.drop(df.columns[list([0, 2])], axis=1, inplace=True)
            df.columns = ['start_position', 'methylation_state']
            unique_positions = unique_positions.union(df['start_position'].tolist())
            # merged = pd.merge(df, merged, how='outer', on='start_position')
            # merged.rename(columns={'methylation_state': file}, inplace=True)
            bar.update(i)
            i += 1
        bar.finish()
        print(len(unique_positions))
        print('pickling... ', end='')
        pickle.dump(merged, open(pickle_path, "wb"))
        print('done')

young_methylation_folder_path = 'MethylationData/Imputed/UD/'
old_methylation_folder_path = 'MethylationData/Imputed/D3/'
young_methylation_df = load_methylation_data(young_methylation_folder_path)
old_methylation_df = load_methylation_data(old_methylation_folder_path)



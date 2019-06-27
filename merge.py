import os
from typing import Set

import pandas as pd
import progressbar

from pickler import load_from_pickle_or_build_and_save_it


def load_and_merge_methylation_data_from_folder_make_closure(folder_path: str):
    def closure() -> pd.DataFrame:
        files = os.listdir(folder_path)
        bar = progressbar.ProgressBar(maxval=len(files),
                                      widgets=[progressbar.Bar('=', '[', ']'),
                                               ' ', progressbar.Percentage()])

        def load_methylation_dataframe_for_file(file) -> pd.DataFrame:
            full_file_path = os.path.join(folder_path, file)
            df = pd.read_csv(full_file_path, sep='\t', header=0)
            df.drop(df.columns[list([0, 2])], axis=1, inplace=True)
            df.columns = ['start_position', 'methylation_state']
            return df

        def get_unique_start_positions_from_folder_make_closure(folder_path: str):
            def closure() -> Set[int]:
                bar.start()
                i = 1
                unique_positions = set()

                for file in files:
                    df = load_methylation_dataframe_for_file(file)
                    unique_positions = unique_positions.union(df['start_position'].tolist())
                    bar.update(i)
                    i += 1
                bar.finish()
                return unique_positions

            return closure

        def get_unique_start_positions_from_folder(folder_path: str) -> Set[int]:
            closure = get_unique_start_positions_from_folder_make_closure(folder_path)
            unique_positions = load_from_pickle_or_build_and_save_it(folder_path + 'start_positions', closure)
            return unique_positions

        unique_positions = get_unique_start_positions_from_folder(folder_path)

        # nan_values = [[np.nan] * len(files)] * len(unique_positions)
        merged = pd.DataFrame(index=sorted(unique_positions), columns=[files])

        bar.start()
        start_positions_to_indexes = dict()
        i = 0
        for start_position in unique_positions:
            start_positions_to_indexes[start_position] = i
            i += 1
        i = 1
        for file in files:
            df = load_methylation_dataframe_for_file(file)
            for index, row in df.iterrows():
                row_index = start_positions_to_indexes[row['start_position']]
                column_index = i - 1
                value = row['methylation_state']
                merged.iat[row_index, column_index] = value
            bar.update(i)
            i += 1
        bar.finish()
        return merged

    return closure


def load_and_merge_methylation_data_from_folder(folder_path: str) -> pd.DataFrame:
    closure = load_and_merge_methylation_data_from_folder_make_closure(folder_path)
    df = load_from_pickle_or_build_and_save_it(folder_path + 'methylation_data', closure)
    return df


young_methylation_folder_path = 'MethylationData/Imputed/UD/'
old_methylation_folder_path = 'MethylationData/Imputed/D3/'
young_methylation_df = load_and_merge_methylation_data_from_folder(young_methylation_folder_path)
old_methylation_df = load_and_merge_methylation_data_from_folder(old_methylation_folder_path)

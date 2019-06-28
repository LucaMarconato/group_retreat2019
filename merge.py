import os
from typing import Set

import pandas as pd
import numpy as np
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

        merged = pd.DataFrame(index=unique_positions)
        merged.index.names = ['start_position']
        bar.start()
        start_positions_to_indexes = dict()
        i = 1
        for file in files:
            column = pd.DataFrame(index=unique_positions)
            column.index.names = ['start_position']
            df = load_methylation_dataframe_for_file(file)
            df.set_index(['start_position'], inplace=True)
            merged_column = pd.merge(column, df, how='outer', on='start_position')
            merged_column_duplicates_removed = merged_column.groupby(['start_position']).mean()
            merged = pd.concat([merged, merged_column_duplicates_removed], axis=1)
            merged.rename(columns={merged.columns[-1]: file}, inplace=True)

            # merged[file] = merged_column['methylation_state']
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

# export a .tsv (tab separated values) file
os.makedirs('exported', exist_ok=True)
young_methylation_exported_path = 'exported/young_methylation.tsv'
old_methylation_exported_path = 'exported/old_methylation.tsv'
if not os.path.isfile(young_methylation_exported_path):
    young_methylation_df.to_csv(young_methylation_exported_path, sep='\t')
if not os.path.isfile(old_methylation_exported_path):
    old_methylation_df.to_csv(old_methylation_exported_path, sep='\t')

# read the trascription data
young_transcription_df = pd.read_csv('ExpressionMatrix/exprs_UD.txt', sep='\t')
old_transcription1_known_df = pd.read_csv('ExpressionMatrix/exprs_D3_test.txt', sep='\t')
old_transcription1_unknown_df = pd.read_csv('ExpressionMatrix/exprs_D3_validation_baseLine.txt', sep='\t')
old_transcription_merged_df = old_transcription1_known_df
for column in old_transcription1_unknown_df.columns.values:
    old_transcription_merged_df[column] = old_transcription1_unknown_df[column]
    old_transcription_merged_df[column] = [np.nan] * len(old_transcription_merged_df)

# read the annotation data
transcription_annotation_df = pd.read_csv('Annotation/featureAnnotation.txt', sep='\t')
single_cell_annotation_df = pd.read_csv('Annotation/relevantCellAnnotation.txt', sep='\t')

print('done')

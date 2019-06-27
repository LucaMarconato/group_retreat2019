import hashlib
import os
import pickle


def load_from_pickle_or_build_and_save_it(pickle_name: str, build_data):
    pickle_file_path = 'pickles/' + hashlib.sha224(pickle_name.encode('utf-8')).hexdigest() + '.pickle'
    if os.path.isfile(pickle_file_path):
        print('loading pickle... ', end='', flush=True)
        data = pickle.load(open(pickle_file_path, 'rb'))
        print('done')
    else:
        data = build_data()
        os.makedirs('pickles', exist_ok=True)
        pickle.dump(data, open(pickle_file_path, 'wb'))
    return data

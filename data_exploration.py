import os
import cv2
import matplotlib.pyplot as plt


def data_exploration(data_dir="data"):
    resp = os.walk(data_dir)
    all_folders = []
    folder_path_to_explore = []

    for (dirpath, dirnames, filenames) in resp:
        all_folders = dirnames
        break

    print("Total Folders inside Directory = ", len(all_folders), all_folders)

    for folder in all_folders:
        files = os.walk(data_dir + "/" + folder)
        for (dirpath, dirnames, filenames) in files:
            if len(filenames):
                print("dirpath ", dirpath, "have file count :", len(filenames))
                folder_path_to_explore.append(dirpath)

    print(folder_path_to_explore)

    return folder_path_to_explore


def load_meta_data(path_to_explore):
    meta_data = {}

    for path in path_to_explore:
        print("Getting meta data for ", os.path.normpath(path))
        path_key = os.path.normpath(path).split("\\")[1]
        for (dirpath, dirnames, filenames) in os.walk(path):
            for filename in filenames:
                f_name = filename.split('.')[0]
                if meta_data.get(f_name):
                    meta_data[f_name][path_key] = os.path.join(os.path.normpath(dirpath), filename)
                else:
                    meta_data[f_name] = {path_key: os.path.join(os.path.normpath(dirpath), filename)}

    print("Collected Meta data for ", len(meta_data), "files")
    return meta_data


# paths = data_exploration()
# meta_data_ = load_meta_data(paths)

import os
import shutil

import pandas as pd


def create_req_dirs(os_dir):
    if not os.path.exists(os_dir):
        os.makedirs(os_dir)
    if not os.path.exists(os_dir + '/images'):
        os.makedirs(os_dir + '/images')
    if not os.path.exists(os_dir + '/labels'):
        os.makedirs(os_dir + '/labels')
    if not os.path.exists(os_dir + '/visuals'):
        os.makedirs(os_dir + '/visuals')


def convert_csv_to_yolo_txt(csv_path, dest_path, img_height=1088, img_width=1920):
    try:
        csv_df = pd.read_csv(csv_path, header=None)
    except Exception as e:
        print('Exception occured while reading csv :', csv_path, e)
        csv_df = pd.DataFrame()

    yolo_boxes = []

    for i, row in csv_df.iterrows():
        left = row[0]
        top = row[1]
        right = row[2]
        bottom = row[3]
        label = 100 if int(row[4]) == 255 else int(row[4])

        center_x = ((left + right) / 2) / img_width
        center_y = ((top + bottom) / 2) / img_height
        width = (right - left) / img_width
        height = (bottom - top) / img_height

        yolo_box = f"{label} {center_x} {center_y} {width} {height}"

        yolo_boxes.append(yolo_box)

    try:
        with open(dest_path, 'w+') as yolo_file:
            yolo_file.write("\n".join(yolo_boxes))
    except Exception as e:
        print(e)


def convert_data_to_yolo_format(meta_data, o_dir):
    if not len(os.listdir(o_dir + '/images/')) == 0:
        print("/images Directory is not empty")
    else:
        for key in meta_data.keys():
            image_src_path = meta_data[key]['images']
            image_dst_path = os.path.normpath(o_dir + '/images/' + key + '.jpg')
            shutil.copy(image_src_path, image_dst_path)

    if not len(os.listdir(o_dir + '/labels/')) == 0:
        print("/labels Directory is not empty")
    else:
        for key in meta_data.keys():
            csv_src_path = meta_data[key]['bboxes']
            txt_dst_path = os.path.join('./' + o_dir + '/labels/' + key + '.txt')
            convert_csv_to_yolo_txt(csv_src_path, txt_dst_path)

import os

import matplotlib.pyplot as plt
import cv2
import pandas as pd

from labels import label_data


def visualize_sample(meta_data, key='vwg-1361-0006'):
    plt.figure(figsize=(15, 15))
    title = ["Input Image", "True Mask"]
    plt.subplot(1, 2, 1)
    plt.title(title[0])
    plt.imshow(cv2.imread(meta_data[key]['images']))
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.title(title[1])
    plt.imshow(cv2.imread(meta_data[key]['labelIds']))
    plt.axis("off")

    plt.show()


def visualize_bounding_box(image_path, box_path, visual_path):
    image = cv2.imread(image_path)

    bboxes = []
    with open(box_path, 'r') as file:
        for line in file.readlines():
            parts = line.strip().split()
            class_id = int(parts[0])  # Class ID
            center_x = float(parts[1])  # Center X
            center_y = float(parts[2])  # Center Y
            width = float(parts[3])  # Width
            height = float(parts[4])  # Height
            bboxes.append((class_id, center_x, center_y, width, height))

    for bbox in bboxes:
        class_id, center_x, center_y, width, height = bbox

        # Convert YOLO format to pixel values
        img_height, img_width = image.shape[:2]
        left = int((center_x - width / 2) * img_width)
        top = int((center_y - height / 2) * img_height)
        right = int((center_x + width / 2) * img_width)
        bottom = int((center_y + height / 2) * img_height)

        label, color = label_data.get(class_id)

        # Draw the rectangle
        cv2.rectangle(image, (left, top), (right, bottom), color, 2)
        # Add label text
        cv2.putText(image, label, (left, top - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    print(visual_path)
    cv2.imwrite(visual_path, image)


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
        label = row[4]

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


def visualize_bounding_box_2(image_path, box_path, visual_path):
    image = cv2.imread(image_path)
    bboxes = pd.read_csv(box_path, header=None)
    image_name = image_path.split('\\')[-1]


    print(image_name)

    visual_path = f"{visual_path}/{image_name}"
    visual_path = os.path.normpath(visual_path)

    for i, row in bboxes.iterrows():
        left = row[0]
        top = row[1]
        right = row[2]
        bottom = row[3]
        class_id = int(row[4])
        label, color = label_data.get(class_id)
        cv2.rectangle(image, (left, top), (right, bottom), color, thickness=5)
        cv2.putText(image, label, (left, top - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 5)

    print(visual_path)
    cv2.imwrite(visual_path, image)

    plt.figure(figsize=(15, 15))
    plt.subplot(1, 2, 1)
    plt.title("Image with bounding box")
    plt.imshow(image)
    plt.axis("off")

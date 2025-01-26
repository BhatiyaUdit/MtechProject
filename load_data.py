import os

import cv2


def load_data_yolo(image_folder, bbox_folder):
    images_data = []
    bounding_box_count = 0
    for image_path in os.listdir(image_folder):
        image = cv2.imread(image_folder + '/' + image_path)

        box_file_name = os.path.splitext(image_path)[0] + '.txt'
        box_file_path = os.path.join(bbox_folder, box_file_name)

        if os.path.exists(box_file_path):
            with open(box_file_path, 'r') as box_file:
                bounding_boxes = []

                for line in box_file.readlines():
                    parts = line.strip().split()
                    class_id = int(parts[0])  # Class ID
                    center_x = float(parts[1])  # Center X
                    center_y = float(parts[2])  # Center Y
                    width = float(parts[3])  # Width
                    height = float(parts[4])  # Height
                    bounding_boxes.append({
                        'label_id': class_id,
                        'left': center_x,
                        'top': center_y,
                        'right': width,
                        'bottom': height
                    })

                    bounding_box_count += 1

        images_data.append((image_path, image, bounding_boxes))

        # break

    print("TOTAL BOUNDING BOXES :", bounding_box_count)
    print("TOTAL IMAGES LOADED : ", len(images_data))
    return images_data
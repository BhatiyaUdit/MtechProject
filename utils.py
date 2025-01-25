import matplotlib.pyplot as plt
import cv2


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

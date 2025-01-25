import os
import tarfile

import requests
from tqdm import tqdm


def download_data(data_root="data"):
    url_prefix = 'https://vitro-testing.com/wp-content/uploads/2022/12/'
    os.makedirs(data_root, exist_ok=True)

    if not len(os.listdir(data_root)) == 0:
        print("Directory is not empty")
        return

    file_names = ['cropandweed_annotations', 'cropandweed_images1of4',
                  'cropandweed_images2of4', 'cropandweed_images3of4',
                  'cropandweed_images4of4']

    for file_name in tqdm(file_names, desc='downloading and extracting files'):
        response = requests.get(f'{url_prefix}{file_name}.tar', stream=True)

        archive = tarfile.open(fileobj=response.raw, mode='r|')
        archive.extractall(data_root)

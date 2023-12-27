import json
import os
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlretrieve

import tensorflow_datasets as tfds
from tqdm.autonotebook import tqdm

# noinspection PyUnresolvedReferences
import sign_language_datasets.datasets
from sign_language_datasets.datasets.config import SignDatasetConfig


# Define a function to decode bytes to string
def decode_bytes(data):
    return data.numpy().decode('utf-8')


# Configuration for the dataset to be loaded
config = SignDatasetConfig(name="2023-11-08", version="1.0.0", include_video=False)
signbank = tfds.load(name='sign_bank', builder_kwargs={"config": config})

# Filter Swiss French sign language data from the dataset
ssr_data = [
    datum for datum in signbank["train"]
    if decode_bytes(datum['country_code']) == "ch" and
       decode_bytes(datum['assumed_spoken_language_code']) == "fr"
]

# Directory to store images
dir_path = "illustrations"
os.makedirs(dir_path, exist_ok=True)
existing_images = set(os.listdir(dir_path))
print("Existing", len(existing_images))

# Skip downloading images that already exist
num_to_skip = len(existing_images)
should_retrieve = []

# Prepare list of files to be downloaded
for datum in ssr_data:
    example_id = decode_bytes(datum["id"])
    file_name = f"{example_id}.png"

    if num_to_skip > 0:
        if file_name in existing_images:
            num_to_skip -= 1
    else:
        if file_name not in existing_images:
            puddle_id = datum["puddle"]
            url = f"https://www.signbank.org/signpuddle2.0/data/sgn/{puddle_id}/{file_name}"
            should_retrieve.append([url, f"{dir_path}/{file_name}"])


# Function to download a file given a URL and a local path
def download_file(url_path_pair):
    url, local_path = url_path_pair
    try:
        urlretrieve(url, local_path)
    except Exception:
        print(f"Failed to fetch {url}, skipping.")


# Download files using ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=10) as executor:
    list(tqdm(executor.map(download_file, should_retrieve), total=len(should_retrieve)))

# Refresh existing images set after downloading
existing_images = set(os.listdir(dir_path))

# Collect data for saving to JSON
data_to_save = []
for datum in ssr_data:
    example_id = decode_bytes(datum["id"])
    if int(example_id) in [2, 4, 9, 48, 230, 286]:
        continue

    file_name = f"{example_id}.png"

    if file_name in existing_images:
        sign_writing = [decode_bytes(t) for t in datum['sign_writing']]
        if len(sign_writing) > 1:
            print("Skipping because it has too many terms", datum, sign_writing)
            continue

        if len(sign_writing) == 0:
            print("Skipping because no terms", file_name)
            continue

        data_to_save.append({
            "file": f"{dir_path}/{file_name}",
            "fsw": sign_writing[0]
        })

# Save data to JSON file
with open("writing.json", "w") as f:
    json.dump(data_to_save, f)

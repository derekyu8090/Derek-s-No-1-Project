import pandas as pd
import os
import requests
from PIL import Image
from io import BytesIO

# Function to download and save an image
def download_and_save_image(url, unique_id, name, category, subclass, base_dir):
    try:
        # Replace any characters in the name that are not valid for filenames
        valid_name = "".join(char for char in name if char.isalnum() or char in [" ", "-", "_"]).rstrip()

        # Filename format: unique_id + name
        filename = f"{unique_id}_{valid_name}.jpg"
        filepath = os.path.join(base_dir, category, f'subclass {subclass}', filename)

        # Download the image
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes

        # Save the image
        image = Image.open(BytesIO(response.content))
        image.save(filepath)

        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

# Load the dataset
file_path = '/Annotated_dataset.csv'
data = pd.read_csv(file_path)

# Create directories for each category and subclass
base_dir = '/Matched images'
for category in data['Category'].unique():
    category_dir = os.path.join(base_dir, category)
    os.makedirs(category_dir, exist_ok=True)
    for subclass in data['subclass'].unique():
        subclass_dir = os.path.join(category_dir, f'subclass {subclass}')
        os.makedirs(subclass_dir, exist_ok=True)

# Iterate over the rows and download images
for index, row in data.iterrows():
    download_and_save_image(row['Image URL'], row['unique_id'], row['Name'], row['Category'], row['subclass'], base_dir)

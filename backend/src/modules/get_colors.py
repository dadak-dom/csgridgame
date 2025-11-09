import os
import random
import cv2
import numpy as np
import pandas as pd
from collections import Counter
from matplotlib import pyplot as plt

data_dir = "C:/Users/dadak/Desktop/personal-projects/csgridgame/data-collector/data/images"  # Change this to your directory
output_csv = "labeled_colors.csv"

def get_dominant_colors(image_path, k=5):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.reshape((-1, 3))
    
    # KMeans clustering to find dominant colors
    from sklearn.cluster import KMeans
    kmeans = KMeans(n_clusters=k, n_init=10)
    kmeans.fit(image)
    
    # Sort colors by frequency
    color_counts = Counter(kmeans.labels_)
    sorted_colors = [tuple(map(int, kmeans.cluster_centers_[i])) for i in color_counts.keys()]
    return sorted_colors

def display_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(image)
    plt.axis('off')
    plt.show()

def label_images():
    if not os.path.exists(data_dir):
        print("Error: Data directory does not exist.")
        return

    images = [f for f in os.listdir(data_dir) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
    if not images:
        print("No images found in directory.")
        return

    existing_data = pd.read_csv(output_csv) if os.path.exists(output_csv) else pd.DataFrame(columns=["image", "color1", "color2", "color3", "color4", "color5"])
    
    random.shuffle(images)
    for image_file in images:
        if image_file in existing_data["image"].values:
            continue
        
        image_path = os.path.join(data_dir, image_file)
        print(f"Labeling: {image_file}")
        display_image(image_path)
        
        dominant_colors = get_dominant_colors(image_path)
        print("Suggested dominant colors (RGB):", dominant_colors)
        
        color_labels = []
        for i in range(5):
            color_name = input(f"Enter color {i+1}: ")
            color_labels.append(color_name)
        
        new_entry = pd.DataFrame([[image_file] + color_labels], columns=["image", "color1", "color2", "color3", "color4", "color5"])
        existing_data = pd.concat([existing_data, new_entry], ignore_index=True)
        existing_data.to_csv(output_csv, index=False)
        print("Data saved.")
        
        cont = input("Label another? (y/n): ")
        if cont.lower() != 'y':
            break

if __name__ == "__main__":
    label_images()

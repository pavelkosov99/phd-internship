import pandas as pd
import matplotlib.pyplot as plt

csv_file_path = 'train.csv'
df = pd.read_csv(csv_file_path)

# Extract the labels and pixel values from the DataFrame
labels = df['label'].values
pixel_values = df.drop('label', axis=1).values

# Create a figure and a grid of subplots
fig, axes = plt.subplots(5, 5, figsize=(10, 10))

# Loop through the first 25 images and display them
for i in range(25):
    ax = axes[i // 5, i % 5]
    image = pixel_values[i].reshape(28, 28)  # Reshape to 28x28 for visualization
    ax.imshow(image, cmap='gray')
    ax.set_title(f"Label: {labels[i]}")
    ax.axis('off')

plt.tight_layout()
plt.show()

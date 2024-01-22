import os

import pandas as pd
import matplotlib.pyplot as plt


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    csv_file_path = os.path.join(current_dir, '../data/csv/test.csv')
    df = pd.read_csv(csv_file_path)

    # Extract pixel values from the DataFrame
    pixel_values = df.values

    # Choose the starting point and range
    starting_point = 25  # Change this to the desired starting point
    range_of_images = 5  # Change this to the desired range

    # Calculate the number of rows and columns based on the range_of_images
    num_cols = min(int(range_of_images ** 0.5), range_of_images)
    num_rows = (range_of_images + num_cols - 1) // num_cols

    # Create a figure and a grid of subplots
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(10, 10))

    # Loop through the selected images and display them
    for i in range(starting_point, min(starting_point + range_of_images, len(pixel_values))):
        row_index = (i - starting_point) // num_cols
        col_index = (i - starting_point) % num_cols
        ax = axes[row_index, col_index]
        image = pixel_values[i].reshape(28, 28)  # Reshape to 28x28 for visualization
        ax.imshow(image, cmap='gray')
        ax.axis('off')

    # Remove empty subplots if there are more rows/columns than needed
    for i in range(range_of_images, num_rows * num_cols):
        fig.delaxes(axes.flatten()[i])

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()

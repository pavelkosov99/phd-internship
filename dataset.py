import torch
import pandas as pd
from PIL import Image

class CustomDataset(torch.utils.data.Dataset):
    def __init__(self, csv_file, transform=None):
        self.dataframe = pd.read_csv(csv_file)
        self.transform = transform

    def __len__(self):
        return len(self.dataframe)

    def __getitem__(self, idx):
        label = self.dataframe.iloc[idx, 0]
        image = self.dataframe.iloc[idx, 1:].values.astype('uint8').reshape(28, 28)
        image = Image.fromarray(image).convert('RGB')
        
        properties = self.label_properties(label)

        if self.transform:
            image = self.transform(image)

        return image, properties

    def label_properties(self, label):
        # Implement your logic here to convert label to properties
        has_circle = 1 if label in [0, 6, 8, 9] else 0
        has_vertical_line = 1 if label in [1, 4, 7, 9] else 0
        has_horizontal_line = 1 if label in [2, 3, 5, 7] else 0
        return torch.tensor([has_circle, has_vertical_line, has_horizontal_line])

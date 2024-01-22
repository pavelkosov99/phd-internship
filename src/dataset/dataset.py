from torch.utils.data import Dataset
import pandas as pd
from PIL import Image


class CustomDataset(Dataset):
    def __init__(self, csv_file, transform=None):
        self.data_frame = pd.read_csv(csv_file)
        self.transform = transform

    def __len__(self):
        return len(self.data_frame)

    def __getitem__(self, idx):
        # Assuming the first column is the label
        label = self.data_frame.iloc[idx, 0]

        # All other columns are pixel values
        image = self.data_frame.iloc[idx, 1:].values.astype('uint8').reshape(28, 28)  # Reshape for MNIST image size
        image = Image.fromarray(image).convert('RGB')

        if self.transform:
            image = self.transform(image)

        return image, label


class CustomTestDataset(Dataset):
    def __init__(self, csv_file, transform=None):
        self.data_frame = pd.read_csv(csv_file)
        self.transform = transform

    def __len__(self):
        return len(self.data_frame)

    def __getitem__(self, idx):
        image = self.data_frame.iloc[idx].values.astype('uint8').reshape(28, 28)
        image = Image.fromarray(image).convert('RGB')

        if self.transform:
            image = self.transform(image)

        return image

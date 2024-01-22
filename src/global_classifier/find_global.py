import os

import torch
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
from src.dataset.dataset import CustomTestDataset
from src.model.model import CustomMultiClassResNet
import json


def load_trained_model(model_path, n_classes):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = CustomMultiClassResNet(n_classes).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    return model


def load_data(csv_file):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    dataset = CustomTestDataset(csv_file=csv_file, transform=transform)
    data_loader = DataLoader(dataset, batch_size=1, shuffle=False)
    return data_loader


def generate_predictions(model, data_loader, output_file):
    model.eval()

    predictions = {}
    device = next(model.parameters()).device

    with torch.no_grad():
        for i, inputs in enumerate(data_loader):
            inputs = inputs.to(device)
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)  # Get the index of the max logit
            predictions[i] = predicted.item()

    with open(output_file, 'w') as f:
        json.dump(predictions, f, indent=4)

    print(f"Predictions saved to {output_file}")


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    model_path = os.path.join(current_dir, '../../data/model/global_model.pth')
    test_csv_file = os.path.join(current_dir, '../../data/csv/test.csv')
    output_file = os.path.join(current_dir, '../../data/json/global_output.json')

    n_classes = 10

    model = load_trained_model(model_path, n_classes)
    test_loader = load_data(test_csv_file)

    generate_predictions(model, test_loader, output_file)


if __name__ == "__main__":
    main()


import os

import torch
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
from src.dataset.dataset import CustomTestDataset
from src.model.model import CustomResNet
import json


def load_trained_model(model_path):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = CustomResNet().to(device)
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


def generate_predictions(circle_model, vertical_line_model, horizontal_line_model, data_loader, output_file):
    circle_model.eval()
    vertical_line_model.eval()
    horizontal_line_model.eval()

    predictions = {}
    image_count = 0

    with torch.no_grad():
        for inputs in data_loader:
            circle_output = circle_model(inputs)
            vertical_line_output = vertical_line_model(inputs)
            horizontal_line_output = horizontal_line_model(inputs)

            image_data = {
                "Circle": bool(circle_output > 0.5),
                "VerticalLine": bool(vertical_line_output > 0.5),
                "HorizontalLine": bool(horizontal_line_output > 0.5)
            }
            predictions[f"Image_{image_count}"] = image_data
            image_count += 1

    with open(output_file, 'w') as file:
        json.dump(predictions, file, indent=4)

    print(f"Properties saved to {output_file}")


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    csv_file = os.path.join(current_dir, '../../data/csv/test.csv')

    circle_model_path = os.path.join(current_dir, "../../data/model/circle_model.pth")
    vertical_line_model_path = os.path.join(current_dir, "../../data/model/vertical_line_model.pth")
    horizontal_line_model_path = os.path.join(current_dir, "../../data/model/horizontal_line_model.pth")

    output = os.path.join(current_dir, '../../data/json/prop_output.json')

    # Load trained models
    circle_model = load_trained_model(circle_model_path)
    vertical_line_model = load_trained_model(vertical_line_model_path)
    horizontal_line_model = load_trained_model(horizontal_line_model_path)

    # Load data for inference
    data_loader = load_data(csv_file)

    # Generate predictions
    generate_predictions(circle_model, vertical_line_model, horizontal_line_model, data_loader, output)


if __name__ == "__main__":
    main()

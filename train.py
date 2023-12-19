import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
import torchvision.transforms as transforms
from dataset import CustomDataset
from model import CustomResNet
import os
import json

def load_data(csv_file, validation_split=0.1):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    dataset = CustomDataset(csv_file=csv_file, transform=transform)
    dataset_size = len(dataset)
    val_size = int(dataset_size * validation_split)
    train_size = dataset_size - val_size
    train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=64, shuffle=False)
    return train_loader, val_loader

def custom_loss(outputs, labels):
    loss_fn = torch.nn.BCELoss()
    return loss_fn(outputs, labels)

def train_and_evaluate(model, train_loader, val_loader, optimizer, num_epochs, model_save_path):
    for epoch in range(num_epochs):
        model.train()
        for inputs, ontology_properties in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = custom_loss(outputs, ontology_properties.float())
            loss.backward()
            optimizer.step()

        # Evaluation phase can be added here if needed
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for inputs, labels in val_loader:
                outputs = model(inputs)
                predicted = (outputs > 0.5).float()
                total += labels.size(0)
                correct += (predicted == labels).type(torch.float).sum().item()

        accuracy = correct / total
        print(f"Epoch {epoch+1}/{num_epochs}, Accuracy: {accuracy:.4f}")

    torch.save(model.state_dict(), model_save_path)

def generate_output_file(model, data_loader, output_file):
    model.eval()
    output_data = {}
    image_count = 1
    with torch.no_grad():
        for images, _ in data_loader:
            outputs = model(images)
            predicted_props = (outputs > 0.5).float()  # Converting probabilities to binary
            for props in predicted_props:
                image_data = {
                    "Circle": bool(props[0]),
                    "VerticalLine": bool(props[1]),
                    "HorizontalLine": bool(props[2])
                }
                output_data[f"Image_{image_count}"] = image_data
                image_count += 1

    with open(output_file, 'w') as file:
        json.dump(output_data, file, indent=4)
                
def main():
    csv_file = 'data/train.csv'
    model_save_path = 'data/model.pth'
    output = 'data/output.json'

    train_loader, val_loader = load_data(csv_file)

    net = CustomResNet()
    
    # Check if a trained model exists
    if os.path.isfile(model_save_path):
        print(f"Loading trained model fro {model_save_path}")
        net.load_state_dict(torch.load(model_save_path))
    else:
        optimizer = optim.Adam(net.parameters(), lr=0.001)
        train_and_evaluate(net, train_loader, val_loader, optimizer, num_epochs=25, model_save_path=model_save_path)

    # Generate the output file for the entire dataset
    generate_output_file(net, train_loader, output)

if __name__ == "__main__":
    main()
import os

import torch
import torch.optim as optim
from torchvision import transforms
from torch.utils.data import DataLoader, random_split
from src.model.model import CustomMultiClassResNet
from src.dataset.dataset import CustomDataset


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
    loss_fn = torch.nn.CrossEntropyLoss()
    return loss_fn(outputs, labels.long())


def train(model, train_loader, val_loader, optimizer, epochs, model_save_path, patience):
    early_stopping_counter = 0
    best_val_loss = float('inf')

    # Determine the device from the model's parameters
    device = next(model.parameters()).device

    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for inputs, labels in train_loader:
            # Convert one-hot encoded labels to class indices if necessary
            if labels.ndim > 1:
                labels = labels.argmax(dim=1)

            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = custom_loss(outputs, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        avg_train_loss = total_loss / len(train_loader)

        # Validation
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                loss = custom_loss(outputs, labels)
                val_loss += loss.item()
        avg_val_loss = val_loss / len(val_loader)

        print(f"Epoch [{epoch + 1}/{epochs}], Training Loss: {avg_train_loss}, Validation Loss: {avg_val_loss}")

        # Early Stopping
        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            early_stopping_counter = 0
            torch.save(model.state_dict(), model_save_path)
        else:
            early_stopping_counter += 1
            if early_stopping_counter >= patience:
                print(f"Early stopping triggered after {patience} epochs with no improvement")
                break


def main():
    # Parameters
    n_classes = 10
    epochs = 25
    patience = 5

    current_dir = os.path.dirname(os.path.abspath(__file__))

    csv_file = os.path.join(current_dir, '../../data/csv/train.csv')
    model_save_path = os.path.join(current_dir, '../../data/model/global_model.pth')

    # Load data
    train_loader, val_loader = load_data(csv_file)

    # Model, Optimizer
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = CustomMultiClassResNet(n_classes).to(device)
    optimizer = optim.Adadelta(model.parameters())

    # Train with Early Stopping
    train(model, train_loader, val_loader, optimizer, epochs, model_save_path, patience)


if __name__ == "__main__":
    main()

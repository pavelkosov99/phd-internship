import os
import src.ontology.create_ontology as create_ontology_file
import src.global_classifier.find_global as find_global
import src.global_classifier.train_global as train_global
import src.dataset.relabel_dataset as relabel_dataset_files
import src.props.train_prop as train_prop
import src.props.find_prop as find_prop
import src.compound_models as compound_models
import src.reasoning as reasoning


def check_file_exists(file_path):
    return os.path.exists(file_path)


# Step 1: Create Ontology by calling the main function from 'create_ontology.py' if 'ontology.owl' doesn't exist.
def create_ontology():
    ontology_file_path = "data/ontology/ontology.owl"
    if not check_file_exists(ontology_file_path):
        create_ontology_file.main()
        print("1 - Create Ontology")


# Step 2: Check if Training and Testing Files exist, and provide a warning if missing.
def check_training_testing_files():
    train_file_path = "data/csv/train.csv"
    test_file_path = "data/csv/test.csv"
    if not (check_file_exists(train_file_path) and check_file_exists(test_file_path)):
        print("Warning: Missing training or testing files (train.csv or test.csv)")
    else:
        print("2 - Training and testing files exist.")


# Step 3: Train the Global Model if it doesn't exist, and then find the Global Model.
def train_and_find_global_model():
    global_model_path = "data/model/global_model.pth"
    if not check_file_exists(global_model_path):
        train_global.main()  # Call the main function from 'train_global.py'
        print("3 - Train Global Model")
    find_global.main()  # Call the main function from 'find_global.py'
    print("3 - Find Global Model")


# Step 4: Relabel the Dataset by calling the main function from 'relabel_dataset.py'
# if specific dataset files don't exist.
def relabel_dataset():
    dataset_paths = [
        "data/csv/props/circle.csv",
        "data/csv/props/horizontal_line.csv",
        "data/csv/props/vertical_line.csv"
    ]
    if any(not check_file_exists(dataset_path) for dataset_path in dataset_paths):
        relabel_dataset_files.main()  # Call the main function from 'relabel_dataset.py'
        print("4 - Relabel Dataset")


# Step 5: Train Prop Models if specific model files don't exist, and then find Prop Models.
def train_and_find_prop_models():
    model_paths = [
        "data/model/circle_model.pth",
        "data/model/vertical_line_model.pth",
        "data/model/horizontal_line_model.pth"
    ]
    if not any(check_file_exists(model_path) for model_path in model_paths):
        train_prop.main()  # Call the main function from 'train_prop.py'
        print("5 - Train Prop Models")
    find_prop.main()  # Call the main function from 'find_prop.py'
    print("5 - Find Prop Models")


# Step 6: Check Output Files - If specific output files don't exist, re-run previous steps as needed.
def check_output_files():
    output_files = [
        "src/json/prop_output.json",
        "src/json/global_output.json",
    ]

    if not check_file_exists(output_files[0]):
        print("Warning: Missing global_output.json files")
        train_and_find_global_model()

    if not check_file_exists(output_files[1]):
        print("Warning:Missing prop_output.json files")
        train_and_find_prop_models()


# Step 7: Run Compound by calling the main function from 'compound.py' if 'compound_output.json' doesn't exist.
def run_compound():
    compound_file_path = "data/json/compound_output.json"
    if not check_file_exists(compound_file_path):
        compound_models.main()
        print("8 - Run Compound")


# Step 8: Run Reasoning
def run_reasoning():
    output_file = "src/json/compound_output.json"
    if not check_file_exists(output_file):
        run_compound()
    reasoning.main()
    print("9 - Run Reasoning")


# Main function
def main():
    create_ontology()
    check_training_testing_files()
    train_and_find_global_model()
    relabel_dataset()
    train_and_find_prop_models()
    check_output_files()
    run_compound()
    run_reasoning()


if __name__ == "__main__":
    main()

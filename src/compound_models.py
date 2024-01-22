import json
import os
import inflect


def load_json(file_name):
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    global_output = load_json(os.path.join(current_dir, '../data/json/global_output.json'))
    prop_output = load_json(os.path.join(current_dir, '../data/json/prop_output.json'))

    compound_output = {}
    for key, image_data in prop_output.items():
        image_number = key.split('_')[1]
        digit = str(global_output.get(image_number, ''))

        p = inflect.engine()
        digit = p.number_to_words(digit)

        properties = [property_name for property_name, property_value in image_data.items() if property_value]

        compound_output[key] = {
            'Digit': digit.title(),
            'hasShape': properties if properties else "No Properties"
        }

    with open(os.path.join(current_dir, '../data/json/compound_output.json'), 'w') as file:
        json.dump(compound_output, file, indent=4)

    print("compound_output.json has been created successfully.")


if __name__ == "__main__":
    main()

import json

# Mapping of word representations to numeric values
word_to_digit = {
    "Zero": 0,
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
    "Six": 6,
    "Seven": 7,
    "Eight": 8,
    "Nine": 9
}

# Load the JSON data
with open('data/solution.json', 'r') as input_file:
    data = json.load(input_file)

# Initialize an empty explanation list
explanations = []

# Iterate over the keys in the JSON (Image_1, Image_2, ...)
for image_key, image_data in data.items():
    possible_properties = []

    # Iterate over the keys in the possible_classes for each image (VerticalLine, HorizontalLine, ...)
    for class_key, class_value in image_data.get('possible_classes', {}).items():
        if class_value:
            possible_properties.append(class_key)

    # Get the possible Digit Classes for the current image
    possible_digit_classes = []
    for class_key in possible_properties:
        possible_digit_classes.extend(data[image_key]['possible_classes'].get(class_key, []))

    # Remove duplicates
    unique_classes = list(set(possible_digit_classes))

    # Sort as words
    unique_sorted_classes = sorted(unique_classes, key=lambda x: word_to_digit.get(x, x))

    # Create the explanation string
    if possible_properties:
        if len(possible_properties) > 1:
            explanation = f"{image_key} possibly has {' and '.join(possible_properties)} property(s) which means that possible Digit Class(es) are/is \"{', '.join(unique_sorted_classes)}\"."
        else:
            explanation = f"{image_key} possibly has {possible_properties[0]} property which means that possible Digit Class(es) are/is \"{', '.join(unique_sorted_classes)}\"."
    else:
        explanation = f"{image_key} has no recognized properties."

    # Add the explanation to the list
    explanations.append(explanation)

# Join the explanations and write them to the explanation.txt file
with open('explanation.txt', 'w') as output_file:
    output_file.write('\n'.join(explanations))
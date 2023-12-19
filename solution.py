import json

# Load the first and second JSON files
with open('data/class_properties.json', 'r') as class_properties:
    data1 = json.load(class_properties)

with open('data/output.json', 'r') as output:
    data2 = json.load(output)

# Initialize the result dictionary
result = {}

# Iterate over the keys in the second JSON (Image_1, Image_2, ...)
for image_key, image_data in data2.items():
    possible_classes = {}

    # Iterate over the keys in the second JSON for each image (Circle, VerticalLine, ...)
    for class_key, class_value in image_data.items():
        # If the class is marked as true in the second JSON
        if class_value:
            # Add the possible classes from the first JSON
            possible_classes[class_key] = data1['hasShape'][class_key]

    # Add the result for this image to the result dictionary
    result[image_key] = {'possible_classes': possible_classes}

# Write the result to the third JSON file
with open('data/solution.json', 'w') as solution:
    json.dump(result, solution, indent=4)

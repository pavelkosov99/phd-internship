from owlready2 import *
import os
import json


def load_json_data(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data


def clean_ontology(onto):
    """ Removes all individuals from the ontology. """
    for individual in list(onto.individuals()):
        destroy_entity(individual)


def update_ontology_with_json(json_data, onto):
    all_shapes = ['Circle', 'HorizontalLine', 'VerticalLine']
    inconsistent_individuals = []

    for image_id, properties in json_data.items():
        digit_class_name = properties["Digit"]
        shapes_present = properties.get("hasShape", [])

        # Create an individual of the specified Digit class
        digit_class = getattr(onto, digit_class_name)
        individual = digit_class(image_id)

        if shapes_present == "No Properties":
            # Add negative assertions for all shapes
            for shape in all_shapes:
                shape_class = getattr(onto, shape)
                individual.is_a.append(Not(onto.hasShape.some(shape_class)))
        else:
            # Assign shapes based on presence or absence
            for shape in all_shapes:
                shape_class = getattr(onto, shape)
                if shape in shapes_present:
                    individual.is_a.append(onto.hasShape.some(shape_class))
                else:
                    individual.is_a.append(Not(onto.hasShape.some(shape_class)))

        # Check consistency
        with onto:
            try:
                sync_reasoner()
            except OwlReadyInconsistentOntologyError:
                # Remove the inconsistent individual
                destroy_entity(individual)
                inconsistent_individuals.append(image_id)

    return inconsistent_individuals


def check_consistency_and_explain(json_data, explanation_file, inconsistent_individuals):
    with open(explanation_file, 'w') as file:
        for image_id, properties in json_data.items():
            digit = properties["Digit"]
            shapes = properties.get("hasShape", [])
            all_shapes = ['Circle', 'HorizontalLine', 'VerticalLine']

            if shapes == "No Properties":
                has_shapes = "no properties"
                not_has_shapes = ', '.join(all_shapes)
            else:
                has_shapes = ' and '.join([shape for shape in shapes])
                not_has_shapes = ' and '.join([shape for shape in all_shapes if shape not in shapes])

            explanation = (f"{image_id} is predicted as {digit} "
                           f"and has {has_shapes}, it does not have {not_has_shapes}.")
            if image_id in inconsistent_individuals:
                explanation = f"{image_id} is NOT consistent and removed from the ontology."
                explanation += (f"However, {image_id} was predicted as {digit} and "
                                f"had {has_shapes}, it did not have {not_has_shapes}.")
            else:
                explanation += f"{image_id} is consistent in the ontology.\n"

            file.write(explanation)


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ontology_path = os.path.join(current_dir, "../data/ontology/ontology.owl")
    json_file_path = os.path.join(current_dir, '../data/json/compound_output.json')
    explanation_file = os.path.join(current_dir, "../explanation.txt")

    # Load the ontology
    onto = get_ontology(ontology_path).load()

    # Clean the ontology from existing individuals
    clean_ontology(onto)

    # Load and parse JSON data
    json_data = load_json_data(json_file_path)

    # Update ontology with JSON data and get list of inconsistent individuals
    inconsistent_individuals = update_ontology_with_json(json_data, onto)

    # Check consistency for each individual and write explanations
    check_consistency_and_explain(json_data, explanation_file, inconsistent_individuals)

    # Save the updated ontology
    onto.save(file=ontology_path, format="rdfxml")


if __name__ == "__main__":
    main()

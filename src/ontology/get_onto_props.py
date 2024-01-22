import os

import owlready2 as owl
from typing import Union
import json


def get_class_leaves(onto_class: owl.entity.ThingClass,
                     max_level: int = -1,
                     current_level: int = 0,
                     return_depth: bool = False) -> list:
    """
    Explores the subclasses of the given class and returns the lowest level subclasses, those
    that have no subclass. If max_level is reached, the subclasses that have this depth are returned.

    :param onto_class: The parent class.
    :param max_level: Maximum level of depth to explore before stopping.
    :param current_level: Used for the recursion stopping condition.
    :param return_depth: Whether to return the depth of each class along with the class.
    :return: A list of the lowest level subclasses, along with their level if return_depth is True.
    """
    # Recursive function, stop if class has no subclass or max level is reached.
    leaf = [onto_class]  # put into iterable so it can be iterated on during the recursion
    subclasses = list(onto_class.subclasses())
    if not subclasses or (0 <= max_level <= current_level):
        if return_depth:
            return [(leaf[0], current_level)]  # leaf contains only one class
        else:
            return leaf
    else:
        leaves = []
        for subclass in onto_class.subclasses():
            leaves += get_class_leaves(subclass, max_level=max_level, current_level=current_level + 1,
                                       return_depth=return_depth)

        return leaves


def get_property_ranges(property: owl.prop.ObjectPropertyClass,
                        depth: int = 1) -> list[owl.entity.ThingClass]:
    """
    Get all classes that are ranges of an object property. Includes all subclasses of a
    class that is a range of the property.

    :param property: The object property to find the ranges of.
    :param depth: The maximum depth of subclasses to explore.
    :return: A list of all classes and their subclasses that are range of the object property.
    """
    ranges = property.range
    res = []
    for range_class in ranges:
        res += get_class_leaves(range_class, max_level=depth, return_depth=False)
    return res


def check_relation(restriction: Union[owl.entity.ThingClass, owl.class_construct.ClassConstruct],
                   property: owl.prop.ObjectPropertyClass, object: owl.entity.ThingClass) -> bool:
    """
    Checks if a given relation corresponds to a restriction of type ObjectProperty.some(object).
    This function is used to find if a given class is a subclass of
    the specific restriction ObjectProperty.restriction(object) where restriction can be any restriction.
    The function also checks the relations of ancestors.

    :param restriction: The restriction to check, usually an element of Class.is_a or Class.equivalent_to.
    :param property: The object property to find in the relation.
    :param object: The class subject of the relation.
    :return: Whether the relation can be found in the given restriction.
    """

    # if restriction is not an instance of ClassConstruct, then it contains no object property, it usually corresponds
    # to a class.
    if isinstance(restriction, owl.class_construct.ClassConstruct):
        # if it is an instance of Restriction, then it corresponds to what we are looking for.
        # if not, restriction may be of the form And([restriction1, restriction2]). If it is Not() then the relation is
        # false. For other types, such as And() and Or(), check the inner restrictions.
        if isinstance(restriction, owl.class_construct.Restriction):
            return restriction.__dict__["property"] == property and restriction.__dict__["value"] == object
        elif isinstance(restriction, owl.class_construct.LogicalClassConstruct):
            # if of the form [restriction1 & restriction2 &...],
            # inner_restriction are obtained with .Classes of the main restriction.
            # Check for the relation recursively inside these inner restrictions.
            return any(
                [check_relation(inner_restriction, property, object) for inner_restriction in restriction.Classes])
        else:
            return False
    else:
        return False


def get_classes_triplet(ontology: owl.namespace.Ontology,
                        property: owl.prop.ObjectPropertyClass,
                        object: owl.entity.ThingClass,
                        only_child: bool = True,
                        ignore_classes: list[owl.ThingClass] = []) -> list[owl.entity.ThingClass]:
    """
    Gets all classes that have a restriction corresponding to property.Restriction(object).
    For example, this function will return every class that is defined by a
    relation such as hasProperty.some(Class). The definition includes the definitions of parent classes.
    If one ancestor of a class has the relation that is searched, this class will be returned.
    When the argument only_child is true, it returns only the descendants, otherwise it will return the ancestors
    as well.

    :param ontology: The ontology, in order to access every class.
    :param property: The object property to find in the relation.
    :param object: The class subject of the relation
    :param only_child: If True, returns only the bottom-level classes i.e. the classes that have no descendants.
            Otherwise, returns every class and its descendants.
    :param ignore_classes: Classes to be ignored when getting class properties.
    :return: A list of all the classes that contain the given relation.
    """
    classes = ontology.classes()
    object_descendants = object.descendants()
    has_prop = []
    for cls in classes:
        # if range_class ancestor in ignore_classes, then skip class
        if [i for i in list(cls.ancestors()) if i in ignore_classes]:
            continue
        if only_child and list(cls.subclasses()):
            # if class has a descendant, ignore to have only last "leaves" when only_child is True
            continue
        all_relations = list(cls.INDIRECT_is_a) + list(
            cls.INDIRECT_equivalent_to)  # INDIRECT is to get restrictions from ancestors
        for relation in all_relations:
            cls_has_prop = False
            for descendant in object_descendants:
                # if a subclass of object is the subject of the relation, then object is also
                # the subject of the relation.
                cls_has_prop = check_relation(relation, property, descendant)
                if cls_has_prop:
                    break

            if cls_has_prop:
                # the relation can only be found once, so we exit the loop if found.
                has_prop.append(cls)
                break
    return has_prop


# MAIN MAIN MAIN MAIN MAIN
def get_class_properties(ontology: owl.namespace.Ontology,
                         main_property: owl.prop.ObjectPropertyClass,
                         ignore_classes: list[owl.ThingClass] = []):
    """
    Finds every subproperty of main_property and gets all their ranges, including subclasses of main ranges.
    Then, for all ranges of one property, finds all classes that have the relation property.Restriction(range).

    :param ontology: The ontology to explore.
    :param main_property: The parent property, only the subproperty of this property will be explored.
    :param ignore_classes: Classes to be ignored when getting class properties.
    :return: A dictionary associating each property with their ranges and maps these ranges with a list of class
            that are defined by the relation property.Restriction(range).
    """
    object_properties_dict = {}

    for op in main_property.subclasses():
        object_properties_dict[op.name] = {}
        property_ranges = get_property_ranges(op, depth=-1)
        for range_class in property_ranges:
            triplets = get_classes_triplet(ontology, op, range_class, ignore_classes=ignore_classes)
            if triplets:
                object_properties_dict[op.name][range_class.name] = [cls.name for cls in triplets]

    # Convert the dictionary to a JSON string
    json_data = json.dumps(object_properties_dict, indent=4)

    # Write the JSON data to a file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir, '../../data/json/onto_props.json'), 'w') as json_file:
        json_file.write(json_data)


def main():
    # Load the ontology
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ontology_path = os.path.join(current_dir, '../../data/ontologies/ontology.owl')

    ontology = owl.get_ontology(ontology_path)
    ontology.load()

    # Define the main property as an object property class
    main_property = ontology.VisualProperty

    print(get_class_properties(ontology, main_property))


if __name__ == '__main__':
    main()

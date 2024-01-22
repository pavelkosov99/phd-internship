from owlready2 import *
import os


def ontology_builder(output_path):
    onto = get_ontology("http://example.org/ontology#")

    with onto:
        # Main Digit Class
        class Digit(Thing):
            pass

        # Main Shape Class
        class Shape(Thing):
            pass

        # Object Properties
        class VisualProperty(ObjectProperty):
            pass

        class hasShape(VisualProperty):
            domain = [Digit]
            range = [Shape]

        # Shape Sub Classes
        class VerticalLine(Shape):
            pass

        class HorizontalLine(Shape):
            pass

        class Circle(Shape):
            pass

        # Digit Sub Classes
        class Zero(Digit):
            is_a = [
                hasShape.some(Circle)
                & Not(hasShape.some(VerticalLine))
                & Not(hasShape.some(HorizontalLine))
            ]

        class One(Digit):
            is_a = [
                hasShape.some(VerticalLine)
                & Not(hasShape.some(Circle))
                & Not(hasShape.some(HorizontalLine))
            ]

        class Two(Digit):
            is_a = [
                hasShape.some(HorizontalLine)
                & Not(hasShape.some(Circle))
                & Not(hasShape.some(VerticalLine))
            ]

        class Three(Digit):
            is_a = [
                Not(hasShape.some(Circle))
                & Not(hasShape.some(HorizontalLine))
                & Not(hasShape.some(VerticalLine))
            ]

        class Four(Digit):
            is_a = [
                hasShape.some(VerticalLine)
                & hasShape.some(HorizontalLine)
                & Not(hasShape.some(Circle))
            ]

        class Five(Digit):
            is_a = [
                hasShape.some(VerticalLine)
                & hasShape.some(HorizontalLine)
                & Not(hasShape.some(Circle))
            ]

        class Six(Digit):
            is_a = [
                hasShape.some(Circle)
                & Not(hasShape.some(HorizontalLine))
                & Not(hasShape.some(VerticalLine))
            ]

        class Seven(Digit):
            is_a = [
                hasShape.some(VerticalLine)
                & hasShape.some(HorizontalLine)
                & Not(hasShape.some(Circle))
            ]

        class Eight(Digit):
            is_a = [
                hasShape.some(Circle)
                & Not(hasShape.some(HorizontalLine))
                & Not(hasShape.some(VerticalLine))
            ]

        class Nine(Digit):
            is_a = [
                hasShape.some(Circle)
                & Not(hasShape.some(HorizontalLine))
                & Not(hasShape.some(VerticalLine))
            ]

        try:
            sync_reasoner()
            onto.save(output_path, format="rdfxml")
            return True
        except OwlReadyInconsistentOntologyError as error:
            return error


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_dir, "../../data/ontology/ontology.owl")
    ontology_builder(output_path)


if __name__ == "__main__":
    main()

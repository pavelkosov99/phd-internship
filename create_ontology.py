from owlready2 import *

def ontology_builder(output_path):
    onto = get_ontology("http://example.org/ontology#")

    with onto:
        # Main Digit Class
        class Digit(Thing):
            pass

        # Main Property Class
        class Property(Thing):
            pass

        # Object Properties
        class VisualProperty(ObjectProperty):
            pass

        class hasShape(VisualProperty):
            domain = [Digit]
            range = [Property]

        # Property Sub Classes
        class VerticalLine(Property):
            pass

        class HorizontalLine(Property):
            pass

        class Circle(Property):
            pass

        # Digit Sub Classes
        class Zero(Digit):
            is_a = [
                hasShape.exactly(1, Circle)
                & Not(hasShape.some(VerticalLine))
                & Not(hasShape.some(HorizontalLine))
            ]

        class One(Digit):
            is_a = [hasShape.exactly(1, VerticalLine) & Not(hasShape.some(Circle))]

        class Two(Digit):
            is_a = [Not(hasShape.some(Circle))]

        class Three(Digit):
            is_a = [Not(hasShape.some(Circle))]

        class Four(Digit):
            is_a = [
                hasShape.min(1, VerticalLine)
                & hasShape.min(1, HorizontalLine)
                & Not(hasShape.some(Circle))
            ]

        class Five(Digit):
            is_a = [
                hasShape.some(VerticalLine)
                & hasShape.some(HorizontalLine)
                & Not(hasShape.some(Circle))
            ]

        class Six(Digit):
            is_a = [hasShape.exactly(1, Circle)]

        class Seven(Digit):
            is_a = [
                hasShape.exactly(1, VerticalLine)
                & hasShape.some(HorizontalLine)
                & Not(hasShape.some(Circle))
            ]

        class Eight(Digit):
            is_a = [hasShape.exactly(2, Circle)]

        class Nine(Digit):
            is_a = [hasShape.exactly(1, Circle)]

        try:
            sync_reasoner()
            onto.save(output_path, format="rdfxml")
            return True
        except OwlReadyInconsistentOntologyError as error:
            return error


ontology_builder("data/ontology.owl")

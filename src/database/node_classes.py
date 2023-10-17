from neomodel import (  # https://neomodel.readthedocs.io/en/latest/index.html
    ArrayProperty, OneOrMore, RelationshipTo, StringProperty, StructuredNode, FloatProperty, RelationshipFrom,
    BooleanProperty)


class Location(StructuredNode):
    """
    Class to represent a general location node.
    """
    nodeId = StringProperty()
    name = StringProperty(unique_index=True, required=True)
    level = StringProperty()
    longitude = FloatProperty()
    latitude = FloatProperty()
    located_in = RelationshipTo("Location", "LOCATED_IN")


class Continent(Location):
    # Create the Continent class as a subclass of Location - https://stackoverflow.com/a/56778266
    """
    Class to represent a continent location node.
    """
    area = StringProperty()  # TODO: Add a API to add the area


class Country(Location):
    # Create the Country class as a subclass of Location - https://stackoverflow.com/a/56778266
    """
    Class to represent a country location node.
    """
    # TODO: Add in "OneOrMore as a third variable below to force a one-to-many relationship"


class County(Location):
    # Create the County class as a subclass of Location - https://stackoverflow.com/a/56778266
    """
    Class to represent a county location node.
    """
    # TODO: Add in "OneOrMore as a third variable below to force a one-to-many relationship"


class State(Location):
    # Create the State class as a subclass of Location - https://stackoverflow.com/a/56778266
    """
    Class to represent a state location node.
    """
    # TODO: Add in "OneOrMore as a third variable below to force a one-to-many relationship"


class City(Location):
    # Create the City class as a subclass of Location - https://stackoverflow.com/a/56778266
    """
    Class to represent a city location node.
    """
    capital = BooleanProperty()
    # TODO: Add in "OneOrMore as a third variable below to force a one-to-many relationship"
    # population = StringProperty()


class Town(Location):
    # Create the Town class as a subclass of Location - https://stackoverflow.com/a/56778266
    """
    Class to represent a town location node.
    """
    # TODO: Add in "OneOrMore as a third variable below to force a one-to-many relationship"
    # population = StringProperty()


class Island(Location):
    # Create the Island class as a subclass of Location - https://stackoverflow.com/a/56778266
    """
    Class to represent an island location node.
    """


class Holiday(StructuredNode):
    """
    Class to represent a holiday note node.
    """
    nodeId = StringProperty(unique_index=True, required=True)
    name = StringProperty(unique_index=True, required=True)
    dateYear = StringProperty(required=True)
    dateMonth = StringProperty(required=True)
    attendees = ArrayProperty()
    text = StringProperty()
    textBodyText = StringProperty()
    textHtmlContent = StringProperty()
    locations = ArrayProperty()
    coverPhoto = StringProperty()
    travelled_to = RelationshipTo(Location, "TRAVELLED_TO", OneOrMore)
    attended = RelationshipFrom("Person", "ATTENDED")


class Person(StructuredNode):
    """
    Class to represent a person node.
    """
    nodeId = StringProperty()
    name = StringProperty(unique_index=True, required=True)
    textBodyText = StringProperty()
    aliases = StringProperty()

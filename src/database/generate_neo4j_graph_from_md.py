import configparser
import os

import obsidiantools.api as otools  # https://pypi.org/project/obsidiantools/
from neomodel import StructuredNode, config
from node_classes import City, Continent, Country, County, Holiday, Island, Location, Person, State, Town
from pathlib import Path
from time import sleep
from typing import List, Tuple
from functools import partial
from geopy.geocoders import Nominatim
import markdown2


class DatabaseConnector:
    def __init__(self, obsidian_vault: otools.Vault):
        self.vault = obsidian_vault
        self.cities: list[str] = []
        self.continents: list[str] = []
        self.countries: list[str] = []
        self.counties: list[str] = []
        self.holidays: list[str] = []
        self.islands: list[str] = []
        self.persons: list[str] = []
        self.states: list[str] = []
        self.towns: list[str] = []
        self.locations: list[str] = []

    def divide_vault(self) -> None:
        """
        function to sort the vault by given tags (labels) and make the data behind the labels iterable.
        """
        for node in self.vault.graph.nodes:
            try:
                frontmatter = vault.get_front_matter(node)
                tags = frontmatter["tags"]
                if "city" in tags:
                    self.cities.append(node)
                elif "continent" in tags:
                    self.continents.append(node)
                elif "country" in tags:
                    self.countries.append(node)
                elif "county" in tags:
                    self.counties.append(node)
                elif "holiday" in tags and not node.startswith("TBC"):
                    self.holidays.append(node)
                elif "island" in tags:
                    self.islands.append(node)
                elif "person" in tags:
                    self.persons.append(node)
                elif "state" in tags:
                    self.states.append(node)
                elif "town" in tags:
                    self.towns.append(node)
                elif "location" in tags:
                    self.locations.append(node)
            except ValueError:
                pass

    @staticmethod
    def remove_brackets(lst: List[str] or str) -> List[str] or str:
        """
        function to remove linking brackets from the frontmatter
        :param lst: list of strings or string that comes from linking data in the frontmatter, e.g. "[[txt]]"
        :return: list of strings or string with [[, ]] removed, e.g. "txt"
        """
        if type(lst) == str:
            return lst.strip("[").strip("]")
        elif type(lst) == list:
            return [item.strip("[").strip("]") for item in lst]

    @staticmethod
    def divide_title(string: str) -> Tuple[int, int, str]:
        """
        function to derive the sub-elements
        :param string: title of a holiday
        :return: tuple of the year, month and name of the holiday
        """
        try:
            [date, name] = string.split(" - ")
            [year, month] = date.split()
            return int(year), int(month), name
        except ValueError:
            pass

    def create_location(self, locations: List[str], node_class: type[StructuredNode]) -> None:
        """
        function to insert locations and their geodata to Neo4j via neomodel
        :param locations: list of locations
        :param node_class: node type
        """
        geocode = partial(Nominatim(user_agent="MyGeocodedTravelJournal/0.0").geocode, language="en")
        for node in locations:
            node_old = node_class.nodes.first_or_none(nodeId=node_class.__name__.lower()+"-"+node)
            if node_old is None:
                loc = geocode(node)
                sleep(1)
                if node_class.__name__ == "City":
                    node_class(name=node, nodeId=node_class.__name__.lower()+"-"+node, level=node_class.__name__,
                               latitude=loc.latitude, longitude=loc.longitude,
                               capital=self.vault.get_front_matter(node)["capital"]).save()
                else:
                    node_class(name=node, nodeId=node_class.__name__.lower()+"-"+node, level=node_class.__name__,
                               latitude=loc.latitude, longitude=loc.longitude).save()

    def connect_locations(self, node_class1: type[StructuredNode] = Location,
                          node_class2: type[StructuredNode] = Location) -> None:
        """
        function to build the relations between all locations
        :param node_class1: optional StructuredNode class
        :param node_class2: optional StructuredNode class
        """
        for node in node_class1.nodes:
            try:
                frontmatter = self.vault.get_front_matter(node.name)
                node.located_in.connect(
                    node_class2.nodes.first_or_none(name=self.remove_brackets(frontmatter['locatedIn'])))
            except KeyError:
                pass

    def create_location_sub_graph(self) -> None:
        """
        function to create the sub-graph of locations
        :return:
        """
        for (loc, node_type) in [(self.continents, Continent), (self.countries, Country), (self.cities, City),
                                 (self.counties, County), (self.islands, Island), (self.states, State),
                                 (self.towns, Town), (self.locations, Location)]:
            self.create_location(loc, node_type)

        self.connect_locations()

    def create_persons(self) -> None:
        """
        function to create all persons
        """
        for node in self.persons:
            node_old = Person.nodes.first_or_none(nodeId=Person.__name__.lower()+"-"+node)
            if node_old is None:
                Person(name=node, nodeId=Person.__name__.lower()+"-"+node).save()

    @staticmethod
    def attend(connect_to: List[str], holiday: Holiday, node_type: type[StructuredNode] = Person) -> None:
        """
        function to connect holidays and persons
        :param connect_to: list of persons
        :param holiday: the holiday they attended
        :param node_type: type of the node
        """
        for connection in connect_to:
            try:
                holiday.attended.connect(
                    node_type.nodes.first_or_none(nodeId=node_type.__name__.lower()+"-"+connection))
            except ValueError:
                pass

    @staticmethod
    def locate(connect_to: List[str], holiday: Holiday, node_type: type[StructuredNode] = Location) -> None:
        """
        function to connect holidays and locations
        :param connect_to: list of locations
        :param holiday: the holiday in which they were visited
        :param node_type: type of the node
        """
        for connection in connect_to:
            try:
                holiday.travelled_to.connect(node_type.nodes.first_or_none(name=connection))
            except ValueError:
                pass

    def create_holiday_sub_graph(self) -> None:
        """
        function to create the holiday nodes and relations
        """
        for node in self.holidays:
            node_old = Holiday.nodes.first_or_none(nodeId=Holiday.__name__.lower()+"-"+node)
            if node_old is None:
                frontmatter = self.vault.get_front_matter(node)
                text = self.vault.get_readable_text(node)
                (year, month, name) = self.divide_title(node)
                attendees = self.remove_brackets(frontmatter["attendees"])
                locations = self.remove_brackets(frontmatter["locations"])
                h = Holiday(name=name, nodeId=Holiday.__name__.lower()+"-"+node, attendees=attendees,
                            coverPhoto=frontmatter["coverPhoto"], dateMonth=month, dateYear=year,
                            locations=locations, textBodyText=text, textHtmlContent=markdown2.markdown(text)).save()
                self.attend(attendees, h)
                self.locate(locations, h)

    def transfer_holiday_vault_to_database(self):
        print("Divide vault by tags")
        self.divide_vault()
        print("Create the location sub-graph")
        self.create_location_sub_graph()
        print("Create the persons")
        self.create_persons()
        print("Create the holiday sub-graph")
        self.create_holiday_sub_graph()


if __name__ == '__main__':
    # Define the relative file path of the config file
    rel_config_file_path = r'..\..\properties.properties'

    # Define the relative folder path of the .md data files
    rel_data_folder_path = r'..\..\database'

    config_file = configparser.ConfigParser()
    config_file.read(rel_config_file_path)

    config.DATABASE_URL = (f'{config_file.get("NEO4J", "N4J.ConnType")}'
                           f'{config_file.get("NEO4J", "N4J.USER")}:'
                           f'{config_file.get("NEO4J", "N4J.PW")}@'
                           f'{config_file.get("NEO4J", "N4J.URL")}/'
                           f'{config_file.get("NEO4J", "N4J.DB")}')
    # Check if the database URL is correct
    # print("config.DATABASE_URL: ", config.DATABASE_URL)

    # Clear the database (only for debugging)
    # db.cypher_query("MATCH (n) DETACH DELETE n")
    # print("'MATCH (n) DETACH DELETE n' sent to clear the database")

    # Connect to the vault of data and gather the tags
    vault = otools.Vault(Path(rel_data_folder_path)).connect().gather()

    con = DatabaseConnector(vault)
    con.transfer_holiday_vault_to_database()

    # Count the number of nodes
    print("Done.")
    node_labels_to_count: list[type[StructuredNode]] = [Continent, Country, County, State,
                                                        City, Town, Island, Holiday, Person, Location]

    [print("   {} Count:  [[{}]]".format(label.__name__, len(label.nodes))) for label in node_labels_to_count]

    print("   {} Count:  [[{}]]".format("Capital", len(City.nodes.filter(capital=True))))

# Holiday Data Transfer Project
This is a hobby project that I created to hone my skills in data extraction, transformation, and loading (ETL) using Python and Neo4j. The project consists of the following steps:

• Extracting data on holidays from an Obsidian vault, which is a personal knowledge management application that uses Markdown files to store notes and links.

•  Transforming the data into a suitable format for Neo4j, which is a graph database that uses nodes, relationships, and properties to store data.

•  Loading the data into Neo4j using the neomodel package, which is an object graph mapper (OGM) that provides a high-level abstraction for working with Neo4j in Python.

Requirements
To run this project, you need to have the following installed on your system:

•  Python 3.9 or higher

•  Obsidian 1.4.16 or higher

•  Neo4j Desktop 1.5.7 or higher

•  obsidiantools 0.10.0 or higher

•  neomodel 5.1.2 or higher

You also need to have an Obsidian vault that contains notes on holidays, such as their names, descriptions, and tags. The notes should follow a consistent format and structure, such as:


title: 2023 10 - Neo4j conference<br>
--- frontmatter<br>
tags: [holiday, autumn]<br>
attendees: [[[Kevin]]]<br>
locations: [[[Earth]]]<br>
--- description<br>
Held a talk on the neo4j conference.

Usage
To run this project, follow these steps:

•  Clone this repository to your local machine using git clone https://github.com/kgruner/NODES-2023-Obsi2Neo4j.git

•  Create a properties.properties file from the template and edit the variables according to your preferences and settings, such as the path to your Obsidian vault (optionally extended), the name of your Neo4j database, and the credentials for connecting to Neo4j.

•  Install the packages of the requirements.txt.

•  Open your Neo4j Desktop application and launch your database.

•  Run the generate_neo4j_graph_from_md.py file. This will execute the ETL process and print some messages to indicate the progress and status of the operation. You should see the nodes and relationships that represent your holiday data in the graph view of the Neo4j database. You can also use Cypher queries to explore and analyze your data further.

License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/grunerkevin/NODES-2023-Obsi2Neo4j/blob/main/LICENSE) file for details.

Acknowledgments
This project was inspired by the following sources:

•  [Obsidian](https://obsidian.md/), a powerful knowledge base that works on top of a local folder of plain text Markdown files.

•  [obsidiantools](https://pypi.org/project/obsidiantools/), a Python package for working with Obsidian vaults.

•  [Neo4j](https://neo4j.com/), a graph database platform that helps you make sense of your data by revealing how people, processes, and systems are interrelated.

•  [neomodel](https://pypi.org/project/neomodel/), a Python package for building applications with Neo4j.

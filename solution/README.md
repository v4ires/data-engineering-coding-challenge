# Data Engineering Coding Challenge

This repository contains the solution for the Data Engineering Coding Challenge by [Your Name].

## Problem Statement

The goal of this coding challenge is to create a Directed Acyclic Graph (DAG) in Airflow that does the following:

1. Parse an XML file and create a graph using the Python NetworkX library.
2. Export the graph to GEXF and GraphML formats.
3. Import the graph into a Neo4j database.

## Prerequisites

- Python 3.8+
- [Apache Airflow](https://airflow.apache.org/) 2.x
- [NetworkX](https://networkx.org/) library
- [Neo4j](https://neo4j.com/) database

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/data-engineering-coding-challenge.git
```

2. Change to the project directory:

```bash
cd data-engineering-coding-challenge
```

3. Go to `solution` folder:

```bash
cd solution
```

4. Create `venv` to install libraries:

```bash
python3 -m venv venv
```

and

```bash
source venv/bin/activate
```

5. Install the required Python libraries:

```bash
pip install -r requirements.txt
```

6. Setup .env file:

Configure the `.env` file based on `.env-example` keys. 
Provide the information needed to execute the scripts:

```bash
NEO4J_URL=
NEO4J_USER=
NEO4J_PASSWORD=
```

7. Set up Airflow:

- Follow the [official Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/start/local.html) to install and set up Apache Airflow.

- Place the `xml_to_neo4j_dag.py` file in your Airflow DAGs folder (usually `$AIRFLOW_HOME/dags`).

- Start the Airflow web server and scheduler.

8. Configure Neo4j:

- Set up a Neo4j instance following the [official Neo4j documentation](https://neo4j.com/docs/operations-manual/current/installation/).

- Update the `utils/neo4j_utils.py` file with your Neo4j database credentials.

9. Modify the input and output paths in the `xml_to_neo4j_dag.py` file.

## Usage

1. Start the Airflow web server and scheduler.

2. Open the Airflow web UI in your browser.

3. Find the `xml_to_neo4j_dag` DAG and enable it.

4. The DAG will run automatically based on the schedule interval. You can also trigger it manually by clicking on the "Play" button.

## Project Structure

- `dags/xml_to_neo4j_dag.py`: The Airflow DAG that defines the workflow for parsing the XML, exporting the graph, and importing it into Neo4j.

- `utils/xml_graph_parser.py`: A utility class that parses the XML file and creates a NetworkX graph.

- `utils/graph_utils.py`: Utility functions for exporting the graph to GEXF and GraphML formats.

- `utils/neo4j_utils.py`: Utility functions for importing the graph into a Neo4j database.

## Jupyter Notebook

> In the `solution/notebooks/data_analysis.ipynb` file, you can find a `Jupyter notebook` that demonstrates the implementation of methods used to convert the `XML` file into a graph representation, export it to different formats, and then import it into a `Neo4j` database.

# Credits

Vinicius Aires Barros - [@v4ires](https://github.com/v4ires)

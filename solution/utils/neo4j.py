import os
import py2neo
import networkx as nx
from py2neo import (Graph, Node, Relationship)


class Neo4J:
    """
    A class to interact with Neo4j graph database using py2neo library.
    """

    def __init__(self) -> None:
        """
        Initialize Neo4j graph instance with connection details.
        """
        
        neo4j_url = os.getenv('NEO4J_URL')
        neo4j_user = os.getenv('NEO4J_USER')
        neo4j_password = os.getenv('NEO4J_PASSWORD')
        self.graph_4j = Graph(neo4j_url, auth=(neo4j_user, neo4j_password))
        

    def create_neo4j_node(self, node: py2neo.Node) -> py2neo.Node:
        """
        Create a py2neo Node object with given properties.

        :param node: A tuple containing the node id and its properties as a dictionary.
        :return: A py2neo Node object with given properties.
        """

        label = 'Node'
        properties = dict(node)
        return Node(label, **properties)

    
    def create_neo4j_relationship(self, source, target, edge) -> py2neo.Relationship:
        """
        Create a py2neo Relationship object with given properties.

        :param source: A py2neo Node object representing the source node.
        :param target: A py2neo Node object representing the target node.
        :param edge: A tuple containing the edge attributes as a dictionary.
        :return: A py2neo Relationship object with given properties.
        """

        rel_type = 'CONNECTED_TO'
        properties = dict(edge)
        return Relationship(source, rel_type, target, **properties)

    
    def import_to_neo4j(self, graph_nx: nx.Graph) -> None:
        """
        Import a NetworkX graph into a Neo4j graph database.

        :param graph_nx: A NetworkX Graph or DiGraph object.
        """

        # Create nodes
        node_mapping = {}
        for node in graph_nx.nodes(data=True):
            n = self.create_neo4j_node(node[1])
            node_mapping[node[0]] = n
            self.graph_4j.create(n)

        # Create relationships
        for edge in graph_nx.edges(data=True):
            source = node_mapping[edge[0]]
            target = node_mapping[edge[1]]
            relationship = self.create_neo4j_relationship(source, target, edge[2])
            self.graph_4j.create(relationship)

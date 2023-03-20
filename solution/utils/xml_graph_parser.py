import itertools
import networkx as nx
from xml.etree import ElementTree
import xml.etree.ElementTree as ET
from utils.graph_utils import export_graph_gexf

class XMLGraphParser:
    """
    Parses an XML file containing protein information and generates a NetworkX graph representing the relationships
    between different elements in the file.

    Args:
        xml_file (str): The path to the XML file to parse.

    Attributes:
        graph (nx.Graph): The NetworkX graph representing the parsed information.
        xml_file (str): The path to the XML file being parsed.
        node_id (itertools.count): An iterator that generates unique node IDs for the graph.
        root (ElementTree.Element): The root element of the XML file being parsed.
        ns (dict): A dictionary mapping the 'uniprot' namespace to its URL.
    """
    
    def __init__(self, xml_file:str) -> None:
        """
        Initializes a new instance of the XMLGraphParser class. The method sets up the graph, loads the XML file
        specified by the `xml_file` parameter, and sets up the default namespace.

        Args:
            xml_file (str): The path to the XML file to be parsed.

        Returns:
            None

        Attributes:
            graph (nx.Graph): A NetworkX graph object representing the parsed information.
            xml_file (str): The path to the XML file being parsed.
            node_id (itertools.count): An iterator that generates unique node IDs for the graph.
            root (ElementTree.Element): The root element of the XML file being parsed.
            ns (dict): A dictionary mapping the 'uniprot' namespace to its URL.
        """
            
        self.graph = nx.DiGraph()
        self.xml_file = xml_file
        self.node_id = itertools.count()
        self.root = ET.parse(self.xml_file).getroot()
        
        # Register default namespace
        self.ns = {'uniprot': 'http://uniprot.org/uniprot'}

        
    def generate_node_id(self) -> int:
        """
        Generates a unique ID for a node in the graph. The method returns an integer value representing the next ID in
        the sequence.

        Args:
            None

        Returns:
            int: The next ID in the sequence.

        """
        
        return next(self.node_id)

    
    def parse_protein_id(self, entry: ElementTree) -> None:
        """
        Parses a protein's ID from an XML element and returns it as a string. The method takes an `entry` argument, which
        is an `ElementTree` object representing a protein in the XML file. The method searches for the first `accession`
        element within the `entry` object, which should contain the protein's ID. If an `accession` element is found, the
        method returns its text value. Otherwise, the method raises an `Exception`.

        Args:
            entry (ElementTree): An `ElementTree` object representing a protein in the XML file.

        Returns:
            str: The protein's ID.

        Raises:
            Exception: If no `accession` element is found in the `entry` object.
        """
            
        accessions = entry.findall(".//uniprot:accession", self.ns)
        if len(accessions) > 0:
            return accessions[0].text
        else:
            raise Exception

            
    def parse_references(self, entry: ElementTree, parent:str) -> None:
        """
        Parses references for a given protein from an XML element and adds them to the graph. The method takes two
        arguments: `entry`, an `ElementTree` object representing a protein in the XML file, and `parent`, a string
        representing the ID of the parent node in the graph to which the references should be added.

        For each reference element in `entry`, the method creates a new node in the graph with the name `Reference`
        and attributes derived from the `citation` element within the reference. The method then adds an edge to the graph
        connecting the reference node to the parent node, with an attribute indicating that the parent node has a
        reference to the reference node. The method then searches for `authorList` elements within the reference, and
        for each author, it creates a new node in the graph with the name `Author` and an attribute for the author's
        name. The method then adds an edge to the graph connecting the reference node to the author node, with an
        attribute indicating that the reference node has an author.

        Args:
            entry (ElementTree): An `ElementTree` object representing a protein in the XML file.
            parent (str): A string representing the ID of the parent node in the graph to which the references should
                be added.

        Returns:
            None
        """
        
        references = entry.findall(".//uniprot:reference", self.ns)
        for ref in references:
            citation = ref.find(".//uniprot:citation", self.ns)
            ref_node_id = self.generate_node_id()
            self.graph.add_node(ref_node_id, name="Reference", attr="\n".join([f"{key}: {value}" for key, value in citation.attrib.items()]))
            self.graph.add_edge(parent, ref_node_id, attr="HAS_REFERENCE")
            author_list = ref.find(".//uniprot:authorList", self.ns)
            for author in author_list:
                author_node_id = self.generate_node_id()
                self.graph.add_node(author_node_id, name="Author", attr=f"name: {author.get('name')}")
                self.graph.add_edge(ref_node_id, author_node_id, attr="HAS_AUTHOR")


    def parse_feature(self, entry: ElementTree, parent:str) -> None:
        """
        Parses features for a given protein from an XML element and adds them to the graph. The method takes two
        arguments: `entry`, an `ElementTree` object representing a protein in the XML file, and `parent`, a string
        representing the ID of the parent node in the graph to which the features should be added.

        For each `feature` element in `entry`, the method creates a new node in the graph with the name `Feature` and
        attributes derived from the `feature` element. The method then adds an edge to the graph connecting the feature
        node to the parent node, with an attribute indicating that the parent node has a feature.

        Args:
            entry (ElementTree): An `ElementTree` object representing a protein in the XML file.
            parent (str): A string representing the ID of the parent node in the graph to which the features should
                be added.

        Returns:
            None
        """
        
        features = entry.findall(".//uniprot:feature", self.ns)
        for fet in features:
            ft_node_id = self.generate_node_id()
            self.graph.add_node(ft_node_id, name="Feature", attr="\n".join([f"{key}: {value}" for key, value in fet.attrib.items()]))
            self.graph.add_edge(parent, ft_node_id, attr="HAS_REFERENCE")
            
            
    def parse_full_name(self, entry: ElementTree, parent:str) -> None:
        """
        Parses a full name for a given protein from an XML element and adds it to the graph. The method takes two
        arguments: `entry`, an `ElementTree` object representing a protein in the XML file, and `parent`, a string
        representing the ID of the parent node in the graph to which the full name should be added.

        If a `fullName` element is found within the `entry` object under `recommendedName`, the method creates a new
        node in the graph with the name `FullName` and an attribute for the full name. The method then adds an edge to
        the graph connecting the full name node to the parent node, with an attribute indicating that the parent node
        has a full name.

        Args:
            entry (ElementTree): An `ElementTree` object representing a protein in the XML file.
            parent (str): A string representing the ID of the parent node in the graph to which the full name should
                be added.

        Returns:
            None
        """

        full_name = self.root.find('.//uniprot:protein/uniprot:recommendedName/uniprot:fullName', self.ns)
        if full_name is not None:
            full_name_node_id = self.generate_node_id()
            self.graph.add_node(full_name_node_id, name="FullName", attr=f"name: {full_name.text}")
            self.graph.add_edge(parent, full_name_node_id, attr="HAS_FULL_NAME")
            
            
    def parse_primary_name(self, entry: ElementTree, parent:str) -> None:
        """
        Parses a primary name for a given protein from an XML element and adds it to the graph. The method takes two
        arguments: `entry`, an `ElementTree` object representing a protein in the XML file, and `parent`, a string
        representing the ID of the parent node in the graph to which the primary name should be added.

        If a `name` element with `type="primary"` is found within the `gene` element under `uniprot`, the method
        creates a new node in the graph with the name `Gene` and an attribute for the primary name. The method then adds
        an edge to the graph connecting the gene node to the parent node, with an attribute indicating that the gene node
        comes from the primary name of the protein.

        Args:
            entry (ElementTree): An `ElementTree` object representing a protein in the XML file.
            parent (str): A string representing the ID of the parent node in the graph to which the primary name should
                be added.

        Returns:
            None
        """

        primary_name = self.root.find('.//uniprot:gene/uniprot:name[@type="primary"]', self.ns)
        if primary_name is not None:
            gene_pri_node_id = self.generate_node_id()
            self.graph.add_node(gene_pri_node_id, name="Gene", attr=f"name: {primary_name.text}")
            self.graph.add_edge(parent, gene_pri_node_id, attr=f"FROM_GENE\nstatus: primary")
            
            
    def parse_synonym_name(self, entry: ElementTree, parent:str) -> None:
        """
        Parses synonym names for a given protein from an XML element and adds them to the graph. The method takes two
        arguments: `entry`, an `ElementTree` object representing a protein in the XML file, and `parent`, a string
        representing the ID of the parent node in the graph to which the synonym names should be added.

        For each `name` element with `type="synonym"` found within the `gene` element under `uniprot`, the method
        creates a new node in the graph with the name `Gene` and an attribute for the synonym name. The method then adds
        an edge to the graph connecting the gene node to the parent node, with an attribute indicating that the gene node
        comes from a synonym name of the protein.

        Args:
            entry (ElementTree): An `ElementTree` object representing a protein in the XML file.
            parent (str): A string representing the ID of the parent node in the graph to which the synonym names should
                be added.

        Returns:
            None
        """
        
        synonym_names = self.root.findall('.//uniprot:gene/uniprot:name[@type="synonym"]', self.ns)
        if synonym_names:
            for synonym_name in synonym_names:
                gene_sec_node_id = self.generate_node_id()
                self.graph.add_node(gene_sec_node_id, name="Gene", attr=f"name: {synonym_name.text}")
                self.graph.add_edge(parent, gene_sec_node_id, attr="FROM_GENE\nstatus: synonym")
            
            
    def parse_scientific_name(self, entry: ElementTree, parent:str) -> None:
        """
        Parses a scientific name and corresponding taxonomy ID for a given protein from an XML element and adds them to
        the graph. The method takes two arguments: `entry`, an `ElementTree` object representing a protein in the XML
        file, and `parent`, a string representing the ID of the parent node in the graph to which the scientific name
        and taxonomy ID should be added.

        The method searches for a `name` element within the `organism` element under `uniprot` with an attribute
        `type="scientific"`, as well as a `dbReference` element with an attribute `type="NCBI Taxonomy"`. If both
        elements are found, it creates a new node in the graph with the name `Organism` and attributes for the
        scientific name and taxonomy ID. The method then adds an edge to the graph connecting the organism node to the
        parent node, with an attribute indicating that the organism node is part of the protein.

        Args:
            entry (ElementTree): An `ElementTree` object representing a protein in the XML file.
            parent (str): A string representing the ID of the parent node in the graph to which the scientific name and
                taxonomy ID should be added.

        Returns:
            None
        """
        
        scientific_name = self.root.find('.//uniprot:organism/uniprot:name[@type="scientific"]', self.ns)
        ncbi_taxonomy_id = self.root.find('.//uniprot:organism/uniprot:dbReference[@type="NCBI Taxonomy"]', self.ns)
        if None not in [scientific_name, ncbi_taxonomy_id]:
            org_node_id = self.generate_node_id()
            self.graph.add_node(
                org_node_id,
                name="Organism",
                attr=f"name: {scientific_name.text}\ntaxonomy_id: {ncbi_taxonomy_id.get('id')}"
            )
            self.graph.add_edge(
                parent, 
                org_node_id,
                attr="IN_ORGANISM"
            )

            
    def parse_protein(self, entry:str) -> None:
        """
        Parses the attributes and related elements of an XML element of a protein, adding them as nodes and edges to the
        graph. The method takes a string argument `entry` representing an XML element of a protein.

        The method first generates a new ID for the protein node and adds it to the graph with the name `Protein` and an
        attribute for the protein ID obtained using the `parse_protein_id` method. It then calls methods to parse and
        add nodes and edges for the protein's full name, primary name and synonym names of the gene, organism,
        references, and features.

        Args:
            entry (str): A string representing an XML element of a protein.

        Returns:
            None
        """
        
        # Find for protein refereces
        protein_node_id = self.generate_node_id()
        self.graph.add_node(protein_node_id, name="Protein", attr=f"id: {self.parse_protein_id(entry)}")

        # Find for full name refereces
        self.parse_full_name(entry, protein_node_id)

        # Find for genes references
        self.parse_primary_name(entry, protein_node_id)

        # Extract synonym names references
        self.parse_synonym_name(entry, protein_node_id)

        # Find for organism references
        self.parse_scientific_name(entry, protein_node_id)

        # Find for references
        self.parse_references(entry, protein_node_id)

        # Find for features
        self.parse_feature(entry, protein_node_id)

        
    def parse(self) -> nx.Graph:
        """
        Parses the entire XML file and builds a graph representation of the data. The method iterates over each XML element
        of a protein in the root of the XML file and calls the `parse_protein` method to parse and add its attributes and
        related elements to the graph. After parsing all proteins, the method returns the resulting graph object.

        Returns:
            nx.Graph: A graph object representing the parsed data.
        """
        
        for entry in self.root.findall(".//uniprot:entry", self.ns):
            self.parse_protein(entry)
        
        return self.graph

import networkx as nx
import matplotlib.pyplot as plt

def plot_graph(graph: nx.Graph) -> None:
    """
    Plots the provided graph using the `networkx` and `matplotlib` libraries. The method draws the nodes and edges of the
    graph and shows the plot on the screen.

    Args:
        graph (nx.Graph): A `networkx` graph object to be plotted.

    Returns:
        None
    """
    
    nx.draw(graph, with_labels=True)
    plt.show()
    
def export_graph_gexf(graph: nx.Graph, file_name:str) -> None:
    """
    Exports the provided graph to a file in the GEXF format using the `networkx` library. The method writes the graph to
    the specified file in the GEXF format, which can be read by many graph visualization tools.

    Args:
        graph (nx.Graph): A `networkx` graph object to be exported.
        file_name (str): A string representing the name of the output file.

    Returns:
        None
    """

    graph_metric = nx.pagerank(graph, weight='weight')
    nx.set_node_attributes(graph, graph_metric, 'pagerank')
    nx.write_gexf(graph, file_name)


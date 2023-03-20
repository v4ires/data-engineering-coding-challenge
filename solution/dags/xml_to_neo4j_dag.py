from datetime import datetime, timedelta
from airflow import DAG

from airflow.operators.python_operator import PythonOperator
from utils.xml_graph_parser import XMLGraphParser
from utils.graph_utils import export_graph_gexf
from utils.neo4j import Neo4J

# Replace these with the paths to your input and output files
input_xml_path = "../../data/Q9Y261.xml"
output_gexf_path = "../data/graph.gexf"

# DAG configuration
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'xml_to_neo4j_dag',
    default_args=default_args,
    description='A DAG to parse XML to a graph, export to GEXF, and import to Neo4j',
    schedule_interval='0 0 * * 1',  # Runs at 00:00 every Monday
    start_date=datetime(2023, 3, 20),  # Set the start date to a recent Monday
    catchup=False,
)

# Task to parse the XML file and create a graph
def parse_xml_to_graph(**kwargs):
    parser = XMLGraphParser(input_xml_path)
    graph = parser.parse()
    kwargs['ti'].xcom_push(key='graph', value=graph)

parse_xml_task = PythonOperator(
    task_id='parse_xml_to_graph',
    python_callable=parse_xml_to_graph,
    provide_context=True,
    dag=dag,
)

# Task to export the graph to GEXF format
def export_graphs(**kwargs):
    graph = kwargs['ti'].xcom_pull(key='graph')
    export_graph_gexf(graph, output_gexf_path)

export_graphs_task = PythonOperator(
    task_id='export_graphs',
    python_callable=export_graphs,
    provide_context=True,
    dag=dag,
)

# Task to import the graph to Neo4j
def import_graph_to_neo4j(**kwargs):
    graph = kwargs['ti'].xcom_pull(key='graph')
    neo4j = Neo4J()
    neo4j.import_to_neo4j(graph, export_graph_gexf, method='gefx')

import_to_neo4j_task = PythonOperator(
    task_id='import_graph_to_neo4j',
    python_callable=import_graph_to_neo4j,
    provide_context=True,
    dag=dag,
)

# Set task order
parse_xml_task >> export_graphs_task >> import_to_neo4j_task

from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
from nytimes_etl import run_nytimes_etl

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',  # Owner of the DAG
    'depends_on_past': False,  # Whether to depend on the success of previous runs
    'start_date': datetime(2024, 10, 15),  # The start date for the DAG execution
    'email': ['gabrielcaldas@live.com'],  # Email address to send notifications
    'email_on_failure': False,  # Whether to send email on task failure
    'email_on_retry': False,  # Whether to send email on task retry
    'retries': 1,  # Number of retries if the task fails
    'retry_delay': timedelta(minutes=1)  # Delay between retries
}

# Define the DAG
dag = DAG(
    'nytimes_dag',  # Unique identifier for the DAG
    default_args=default_args,  # Set the default arguments for the DAG
    description='My ETL code',  # Brief description of the DAG
    schedule_interval='@daily',  # How often the DAG should run (daily in this case)
)

# Define a Python task using the PythonOperator
run_etl = PythonOperator(
    task_id='complete_nytimes_etl',  # Unique identifier for this task
    python_callable=run_nytimes_etl,  # The function to run when the task executes
    dag=dag  # Reference to the DAG that this task belongs to
)

run_etl  # Register the task with the DAG

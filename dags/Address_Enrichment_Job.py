import os
from datetime import datetime
from airflow.decorators import dag, task
from airflow.models import DAG, Variable
from airflow.operators.python import PythonOperator

# import module kamu
from src.utils.reader import read_json
from src.transformers.address_transformer import transform
from src.utils.writer import write_json


# =============================
# CONFIG
# =============================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

INPUT_PATH = os.path.join(BASE_DIR, "data/int_test_input")
OUTPUT_PATH = os.path.join(BASE_DIR, "data/int_test_output/output.json")


# =============================
# TASK FUNCTION
# =============================
def run_address_enrichment():

    input_path = os.path.join(BASE_DIR, INPUT_PATH)

    # 1. Read
    records = read_json(input_path)

    # 2. Transform + Enrich
    enriched = transform(records)

    # 3. Write
    write_json(enriched, OUTPUT_PATH)


# =============================
# DAG DEFINITION
# =============================

@dag(
    dag_id="Address_Enrichment_Job",
    description="Address enrichment using LocationIQ API",
    schedule_interval=None,
    max_active_runs=1,
    default_args = {
    "owner": "wina",
    "retries": 1
},
    start_date=datetime(year=2026, month=2, day=27, hour=0, minute=0, second=0),
    catchup=False
    )

def main_job():
    run_task = PythonOperator(
        task_id="run_address_enrichment",
        python_callable=run_address_enrichment,
    )

    run_task
dag = main_job()
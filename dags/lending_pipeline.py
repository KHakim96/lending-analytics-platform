from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="lending_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["lending", "data-engineering"]
) as dag:

    load_seed_data = BashOperator(
        task_id="load_seed_data",
        bash_command="""
        cd /opt/airflow/project &&
        python src/bootstrap/load_seed_data.py
        """
    )

    extract_parquet = BashOperator(
        task_id="extract_parquet",
        bash_command="""
        cd /opt/airflow/project &&
        python src/extract/postgres_to_parquet.py
        """
    )

    load_snowflake = BashOperator(
        task_id="load_snowflake",
        bash_command="""
        cd /opt/airflow/project &&
        python src/load/snowflake_loader.py
        """
    )
    
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="""
        cd /opt/airflow/project/dbt/lending_analytics &&
        dbt run --profiles-dir /opt/airflow/project/dbt/profiles
        """
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="""
        cd /opt/airflow/project/dbt/lending_analytics &&
        dbt test --profiles-dir /opt/airflow/project/dbt/profiles
        """
    )

    load_seed_data >> extract_parquet >> load_snowflake >> dbt_run >> dbt_test
import json
from datetime import datetime, timedelta
import string

from airflow.decorators import dag, task

from dags_config import Config as config
from custom_operators import (
    FinCubeFactOperator
)

@dag(schedule_interval="1-59 * * * *", start_date=datetime(2021, 1, 1), catchup=False, tags=["example"])
def tutorial_taskflow_api_etl():
    """
    ### Get Reference Rates from New York Fed
    Use open APIs from New York Fed to fetch all reference rates,
    including secured and unsecured ones.
    """
    @task()
    def extract():
        """
        #### Extract task
        A simple Extract task.
        """
        data_string = '{"1001": 301.27, "1002": 433.21, "1003": 502.22}'

        order_data_dict = json.loads(data_string)
        return order_data_dict
    
    @task(multiple_outputs=True)
    def transform(order_data_dict: dict):
        """
        #### Transform task
        A simple Transform task
        """
        total_order_value = 0
        for value in order_data_dict.values():
            total_order_value += value

        return {"total_order_value" : total_order_value}
    
    @task()
    def load(total_order_value: float):
        """
        #### Load task
        A simple Load task.
        """
        print(f"Total order value is: {total_order_value:.2f}")
    
    # the invocation itself automatically generates the deps
    order_data = extract()
    order_summary = transform(order_data)
    load(order_summary["total_order_value"])

@dag(schedule_interval="1-59/10 * * * *", start_date=datetime(2021, 1, 1), catchup=False, tags=["example"])
def fin_cube_fact():
    """
    ### Simulate credit card transactions every 10 seconds
    Generate random numbers and strings for credit card transactions,
    and send them to a Kafka topic.
    """
    @task()
    def start():
        return f"{datetime.now()}:  starting!"

    @task()
    def event(config):
        return FinCubeFactOperator(
            task_id=f"exporting_fact_to_broker",
            validator_config=config.VALIDATOR_CONFIG,
            arr_length=config.ARRAY_LENGTH,
            nb_rows=config.NB_ROWS,
            nb_part=config.NB_PART,
            bootstrap_servers=config.BOOTSTRAP_SERVERS,
            topic=config.TOPIC
        )

    @task()
    def finish():
        return f"{datetime.now()}:  finishing!"

    start()
    event(config)
    finish()


# tutorial_etl_dag = tutorial_taskflow_api_etl()
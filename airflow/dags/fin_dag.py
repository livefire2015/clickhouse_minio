import json
from datetime import datetime, timedelta
import logging

from airflow.decorators import dag, task

from dags_config import Config as config
from fin_cube_fact import (
    FactGenerator,
    FactExporter,
    FactValidator
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

@dag(schedule_interval="1-59/1 * * * *", start_date=datetime(2021, 1, 1), catchup=False, tags=["FinCube"])
def fin_cube_fact():
    validator = FactValidator(config.VALIDATOR_CONFIG)
    generator = FactGenerator(config.ARRAY_LENGTH, config.NB_ROWS, config.NB_PART)

    """
    ### Simulate credit card transactions every 10 seconds
    Generate random numbers and strings for credit card transactions,
    and send them to a Kafka topic.
    """
    @task()
    def start():
        return f"{datetime.now()}:  starting!"

    @task()
    def event():
        with FactExporter(config.BOOTSTRAP_SERVERS) as exporter:
            try:
                for fact in generator.get_fact_stream():
                    logging.info(fact)
                    validator.validate_fact(fact)
                    exporter.export_fact_to_broker(
                        config.TOPIC,
                        fact._asdict()
                    )
            except Exception as err:
                logging.error(f"Exception: {err}")
                raise err

    @task()
    def finish():
        return f"{datetime.now()}:  finishing!"

    st = start()
    facts = event()
    fi = finish()

    st >> facts >> fi


# tutorial_etl_dag = tutorial_taskflow_api_etl()
fin_cube_fact_dag = fin_cube_fact()

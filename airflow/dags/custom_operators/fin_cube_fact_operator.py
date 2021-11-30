from log import log
from retry import RetryOnException as retry
from fin_cube_fact import (
    FactGenerator,
    FactExporter,
    FactValidator
)

from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults


@log
class FinCubeFactOperator(BaseOperator):

    @apply_defaults
    def __init__(
            self,
            validator_config,
            arr_length,
            nb_rows,
            nb_part,
            bootstrap_servers,
            topic,
            *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validator_config = validator_config
        self.arr_length = arr_length
        self.nb_rows = nb_rows
        self.nb_part = nb_part
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic

    @retry(5)
    def execute(self, context):
        validator = FactValidator(self.validator_config)
        generator = FactGenerator(self.arr_length, self.nb_rows, self.nb_part)

        with FactExporter(self.bootstrap_servers) as exporter:
            self.logger.info(self.topic)
            try:
                for fact in generator.get_fact_stream():
                    self.logger.info(fact)
                    validator.validate_fact(fact)
                    exporter.export_fact_to_broker(
                        self.topic,
                        fact._asdict()
                    )
            except Exception as err:
                self.logger.error(f"Exception: {err}")
                raise err

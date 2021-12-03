

class FactValidator:
    def __init__(self, config):
        self._config = config

    def validate_fact(self, fact):
        fact = fact if isinstance(fact, dict) else fact._asdict()
        assert self.check_null_values(fact), "Null values!"

    def check_null_values(self, fact):
        fact_values = list(fact.values())
        return all(v is not None for v in fact_values)

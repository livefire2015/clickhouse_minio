

class FactValidator:
    def __init__(self, config):
        self._config = config

    def validate_fact(self, fact):
        fact = fact.as_dict()
        assert self.check_null_values(fact), "Null values!"

    def check_null_values(self, fact):
        fact_values = list(fact.values())
        return all(fact_values)

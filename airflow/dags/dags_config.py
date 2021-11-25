

class Config:

    ARRAY_LENGTH = 100
    NB_ROWS = 10
    NB_PART = 3

    BOOTSTRAP_SERVERS = ["kafka:9092"]

    TOPIC = "finCube.factTable"

    VALIDATOR_CONFIG = {
        "description_length": 10,
        "languages": [
            "en", "pl", "es", "de"
        ]
    }

    REFERENCE_RATES = {
        "secured": ["https://markets.newyorkfed.org/api/rates/secured/all/latest.xml"],
        "unsecured": ["https://markets.newyorkfed.org/api/rates/unsecured/all/latest.xml"]
    }



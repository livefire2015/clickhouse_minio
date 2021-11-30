import pytest
import pandas as pd

from collections import namedtuple
from requests import Response
from retry import RetryOnException as retry
from fin_cube_fact import FactGenerator, FactValidator


@pytest.fixture
def generator():
    yield FactGenerator(1, 1, 1)


@pytest.fixture
def validator():
    yield FactValidator(
        {
            "description_length": 10,
            "languages": ["en"]
        }
    )


@pytest.fixture
def response():
    def helper(status_code):
        response = Response()
        response.status_code = status_code
        response.headers['Content-Type'] = "text/html"
        return response
    yield helper


@pytest.fixture
def add_function():

    @retry(5)
    def func(a, b):
        return a + b

    yield func

@pytest.fixture
def fact_record():
    Pandas = namedtuple('Pandas', ['int0', 'int33', 'str0', 'str32', 'arrFloat', 'partition'])
    yield  Pandas(int0=-694289, int33=-694, str0='yWAcqGFzYtEwLnGis', str32='yWAcqGFzYtEwLnGis', arrFloat=pd.array([844265.74858102]), partition=0)

@pytest.fixture
def fact_record_bad():
    Pandas = namedtuple('Pandas', ['int0', 'int33', 'str0', 'str32', 'arrFloat', 'partition'])
    yield  Pandas(int0=-694289, int33=None, str0='yWAcqGFzYtEwLnGis', str32='yWAcqGFzYtEwLnGis', arrFloat=pd.array([844265.74858102]), partition=0)

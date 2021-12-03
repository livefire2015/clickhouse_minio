import datetime
from typing import List
from unittest.mock import patch

from pandas._libs.tslibs.timestamps import Timestamp
import numpy as np
import pytest

from ..fixtures import generator


def test_get_fact_stream(generator):

    stream = generator.get_fact_stream()
    result = list(stream)[-1]

    assert result is not None
    assert isinstance(result.int0, int)
    assert isinstance(result.int33, int)
    assert isinstance(result.dttime0, str)
    assert isinstance(result.str0, str)
    assert isinstance(result.str32, str)
    assert isinstance(result.arrFloat, (list, tuple, np.ndarray))
    assert isinstance(result.partition, int)

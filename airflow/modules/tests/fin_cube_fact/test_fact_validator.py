import pytest

from ..fixtures import validator, fact_record, fact_record_bad


def test_check_null_values(validator, fact_record):
    expected = True

    fact = fact_record._asdict()

    result = validator.check_null_values(fact)
    
    assert result is expected


def test_validate_fact_raises_error(validator, fact_record_bad):
    
    with pytest.raises(AssertionError):
        validator.validate_fact(fact_record_bad)

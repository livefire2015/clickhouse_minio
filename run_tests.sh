#!/bin/sh

pip install -r airflow/requirements.txt \
    && py.test airflow/modules/tests/ --doctest-modules --cov airflow/modules --show-capture=no -v
FROM wuuker/docker-airflow:2.2.1

WORKDIR /usr/local/airflow

COPY requirements.txt .

RUN pip install -r requirements.txt 

ENV PYTHONPATH "${PYTHONPATH}:/usr/local/airflow/modules"

ENV EXECUTOR "Local"
ENV AIRFLOW__SCHEDULER__MIN_FILE_PROCESS_INTERVAL "15"
ENV AIRFLOW__WEBSERVER__WORKER_REFRESH_INTERVAL "450"
ENV AIRFLOW__WEBSERVER__WEB_SERVER_WORKER_TIMEOUT "150"

# Add Custom Configuration
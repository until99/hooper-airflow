from datetime import datetime, timedelta
from airflow.sdk import DAG, task, task_group
from pipelines.weather import pipe_weather


@task
def retrieve_history_weather_data():
    return pipe_weather.fetch_history_weather_data("Joinville")


@task
def format_history_weather_data(history_data):
    return pipe_weather.format_history_weather_data(history_data)


@task
def delete_history_weather_data():
    pipe_weather.delete_history_weather_data()


@task
def insert_history_weather_data_into_database(formatted_data):
    pipe_weather.insert_history_weather_data_into_database(formatted_data)


@task_group(group_id="process_historical_weather_data")
def process_historical_weather_data():
    history_data = retrieve_history_weather_data()
    formatted_data = format_history_weather_data(history_data)
    delete_history_weather_data()
    insert_history_weather_data_into_database(formatted_data)


@task
def retrieve_forecast_weather_data():
    return pipe_weather.fetch_forecast_weather_data("Joinville")


@task
def format_forecast_weather_data(forecast_data):
    return pipe_weather.format_forecast_weather_data(forecast_data)


@task
def delete_forecast_weather_data():
    pipe_weather.delete_forecast_weather_data()


@task
def insert_forecast_weather_data_into_database(formatted_data):
    pipe_weather.insert_forecast_weather_data_into_database(formatted_data)


@task_group(group_id="process_forecast_weather_data")
def process_forecast_weather_data():
    forecast_data = retrieve_forecast_weather_data()
    formatted_data = format_forecast_weather_data(forecast_data)
    delete_forecast_weather_data()
    insert_forecast_weather_data_into_database(formatted_data)


with DAG(
    "weather_report",
    default_args={
        "depends_on_past": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
        # 'wait_for_downstream': False,
        # 'execution_timeout': timedelta(seconds=300),
        # 'on_failure_callback': some_function, # or list of functions
        # 'on_success_callback': some_other_function, # or list of functions
        # 'on_retry_callback': another_function, # or list of functions
        # 'sla_miss_callback': yet_another_function, # or list of functions
        # 'on_skipped_callback': another_function, #or list of functions
        # 'trigger_rule': 'all_success'
    },
    description="A simple weather report DAG",
    schedule="0 3 * * *",
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["weather"],
) as dag:
    process_historical_weather_data()
    process_forecast_weather_data()

from __future__ import annotations

from datetime import datetime

from airflow.decorators import dag, task


@dag(start_date=datetime(2024, 1, 1), schedule="@daily", catchup=False)
def example_dag():
    @task
    def extract() -> list[int]:
        return [1, 2, 3]

    @task
    def transform(values: list[int]) -> list[int]:
        return [value * 2 for value in values]

    @task
    def load(values: list[int]) -> None:
        print(values)

    load(transform(extract()))


example_dag()

import textwrap
from datetime import datetime, timedelta, timezone

from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG

with DAG(
    dag_id="tutorial",
    default_args={
        "depends_on_past": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
        # "queue": "bash_queue",
        # "pool": "backfill",
        # "priority_weight": 10,
        # "end_date": datetime(2016, 10, 1),
        # "wait_for_downstream": False,
        # "execution_timeout": timedelta(seconds=300),
        # "on_failure_callback": some_function,  # or list of functions
        # "on_success_callback": some_other_function,  # or list of functions
        # "on_retry_callback": another_function,  # or list of functions
        # "sla_miss_callback": yet_another_function,  # or list of functions
        # "on_skipped_callback": another_function,  # or list of functions
        # "trigger_rule": "all_success",
    },
    description="A simple tutorial DAG",
    schedule=timedelta(days=1),
    # start_date=datetime(2021, 1, 1, tzinfo=timezone.utc),
    start_date=datetime.now(timezone.utc) + timedelta(seconds=10),
    catchup=False,
    tags=["example"],
) as dag:
    # t1, t2 and t3 are examples of tasks created by instantiating operators
    t1 = BashOperator(
        task_id="print_date",
        bash_command="date",
    )

    t2 = BashOperator(
        task_id="sleep",
        depends_on_past=False,
        bash_command="sleep 5",
        retries=3,
    )

    t1.doc_md = textwrap.dedent(
        """\
    ### Task Documentation
    You can document your tasks using the `doc_md` (markdown),
    `doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
    rendered in the UI's Task Instance Details page.
    ![img](https://imgs.xkcd.com/comics/fixing_problems.png)
    **Image Credit:** Randall Munroe, [XKCD](https://xkcd.com/license.html)
    """
    )

    dag.doc_md = __doc__  # providing that you have a docstring at the beginning of the DAG; OR
    dag.doc_md = """
    This is a documentation placed anywhere
    """  # otherwise, type it like this
    template_command = textwrap.dedent(
        """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7) }}"
    {% endfor %}
    """
    )

    t3 = BashOperator(
        task_id="templated",
        depends_on_past=False,
        bash_command=template_command,
    )

    t1 >> [t2, t3]

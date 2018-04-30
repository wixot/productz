from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

from collector.tasks import *

from datetime import datetime, timedelta

a_year_ago = datetime.now() - timedelta(days=3)

default_args = {
    'owner': 'wixot',
    'depends_on_past': False,
    'start_date': a_year_ago,
    'email': ['hello@wixot.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'max_tries': 3,
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('reporting', default_args=default_args, schedule_interval="@daily")

cb = PythonOperator(
    task_id='collect_chartboost',
    python_callable=daily_update_chartboost_app_analytics,
    provide_context=True,
    retries=3,
    dag=dag)

ua = PythonOperator(
    task_id='collect_unity_ads',
    python_callable=daily_update_unityads_revenues,
    provide_context=True,
    retries=3,
    dag=dag)

adm = PythonOperator(
    task_id='collect_admob',
    python_callable=daily_update_admob_revenues,
    provide_context=True,
    retries=3,
    dag=dag)

fb = PythonOperator(
    task_id='collect_facebook',
    python_callable=daily_update_facebook_revenues,
    provide_context=True,
    retries=3,
    dag=dag)

it = PythonOperator(
    task_id='collect_itunes_inapp',
    python_callable=update_itunes_inapp_products,
    provide_context=True,
    retries=3,
    dag=dag)

pl = PythonOperator(
    task_id='collect_play_inapp',
    python_callable=update_play_inapp_products,
    provide_context=True,
    retries=3,
    dag=dag)

vp = PythonOperator(
    task_id='collect_play_inapp',
    python_callable=update_play_inapp_voided_purchases,
    provide_context=True,
    retries=3,
    dag=dag)

cur = PythonOperator(
    task_id='collect_currency_rate',
    python_callable=store_currency_rates,
    provide_context=True,
    retries=3,
    dag=dag)

slp = BashOperator(
    task_id='sleep_one_sec',
    bash_command='sleep 1',
    retries=1,
    dag=dag)

cb.set_upstream(slp)
ua.set_upstream(slp)
adm.set_upstream(slp)
fb.set_upstream(slp)
it.set_upstream(slp)
pl.set_upstream(slp)
cur.set_upstream(slp)
vp.set_upstream(slp)

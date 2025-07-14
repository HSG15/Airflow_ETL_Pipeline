from airflow import DAG
from airflow.providers.http.operators.http import HttpOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook #PostgresHook lets Airflow talk to Postgres.
from airflow.decorators import task #@task allows writing Python functions as Airflow tasks.
#from airflow.utils.dates import days_ago #depricated In Airflow 2.9+
from datetime import datetime, timedelta
import json
import requests #requests is for calling the NASA API.


# Define the DAG
with DAG(
    dag_id = 'proj_nasa_apod_etl',
    #start_date = days_ago(1),
    start_date = datetime.now() - timedelta(days=1), # Use this instead of days_ago
    schedule = '@daily',
    catchup = False
) as dag:
      
    #Step 1 : Create the table if it does not exist
    @task
    def create_table():
        hook = PostgresHook(postgres_conn_id='my_postgres_connection') #initialize the Postgres hook, this connection id will be required during connection in Airflow UI.
        create_table_query = """
            CREATE TABLE IF NOT EXISTS nasa_apod_data (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255),
                explanation TEXT,
                url VARCHAR(255),
                date DATE,
                media_type VARCHAR(50)
            );
        """
        hook.run(create_table_query) #execute the table creation query 


    #Step 2 : Extract/Fetch the data from the NASA API APOD (Astronomy Picture of the Day)
    @task
    def extract_apod():
        api_key = "YmTRPfgn5MakazbczbdVk5eyJIUjNKfUEfkrRiLz" #api.nasa.gov
        url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
        response = requests.get(url) #Hits NASA’s APOD API and returns the JSON response.
        print('Received data from APOD :', response) #Received data from APOD : <Response [200]>: chan="stdout": source="task"
        print('Received JSON data from APOD :', response.json())
        return response.json()

    #Step 3 : Transform the data : Pick information from the response
    @task
    def transform_apod_data(response):
        apod_data = {
            'title' : response.get('title', ''),
            'explanation' : response.get('explanation', ''),
            'url' : response.get('url', ''),
            'date' : response.get('date', ''),
            'media_type' : response.get('media_type', '')
        }
        print('Title of the APOD : ', apod_data['title'])
        return apod_data
    

    #Step 4 : Load the data into the Postgres table
    @task
    def load_data_to_postgres(apod_data):
        postgres_hook = PostgresHook(postgres_conn_id='my_postgres_connection')
        print('Loading data to Postgres table...', apod_data)
        #define the insert query
        insert_query = """
            INSERT INTO nasa_apod_data (title, explanation, url, date, media_type)
            values(%s, %s, %s, %s, %s)
        """

        #Execute the insert query with the data
        postgres_hook.run(insert_query, parameters=(
            apod_data['title'],
            apod_data['explanation'],
            apod_data['url'],
            apod_data['date'],
            apod_data['media_type']
        ))



    #Step 6 : Define the task dependencies
    # ✅ Define task instances using intermediate variables
    create_table_task = create_table()
    extracted = extract_apod()
    transformed = transform_apod_data(extracted)
    loaded = load_data_to_postgres(transformed)

    # ✅ Set task dependency
    create_table_task >> extracted >> transformed >> loaded

'''
# To run this DAG, run below command in the terminal:
    1. astro dev init
    2. astro dev start
    3. astro dev restart
    4. astro dev stop

#errors:
    🚨 Error: error building, (re)creating or starting project containers: Error response from daemon: failed to set up container networking: driver failed programming external 
    connectivity on endpoint proj-etl-pipeline-api-integration_6d3a38-postgres-1 (7b21ea429fb7255e4cd739f85fb5a400df81c80507009b436adfcf8118c15fa5): Bind for 127.0.0.1:5432 failed:
    port is already allocated
    ✅ Solution: 
    lsof -i :5432
    kill -9 <PID>
    astro dev restart
    to deploy to astro dev:
    1. astro login
    2. astro deployment list
    3. astro deploy <deployment_id> -f
    Then It will start pushing the code to the cloud and will show the progress in the terminal.
'''

# 🛢️ I used DBeaver to see the data in the database

'''
| Problem                        | Fix                                               |
| ------------------------------ | ------------------------------------------------- |
| `days_ago` not found           | Replace with `datetime.now() - timedelta(days=1)` |
| `.data` access on task         | ❌ Not possible. Use TaskFlow return values        |
| `HttpOperator` imports fragile | ✅ Better to use `requests.get()` in `@task`       |
'''

# APOD ETL Pipeline

In this project, I built an ETL pipeline using Apache Airflow that pulls data from NASA’s APOD API and stores it in PostgreSQL.

---

## Setting up the Development Environment

I started by creating the project using Astronomer CLI (`astro dev init`), which gave me the base Airflow + Docker setup.  

Inside the project, I wrote a DAG (`etl.py`) with four main tasks:

- **create_table** → ensure the Postgres table exists  
- **extract_apod** → call the NASA API  
- **transform_apod_data** → clean and format the JSON response  
- **load_data_to_postgres** → insert records into Postgres  

---

## Running with Docker Compose

To run everything locally, I used the `docker-compose.yaml` file, where I defined two main services:

- **Airflow service** → exposed on port 8080 (for monitoring DAGs in the web UI)  
- **Postgres service** → exposed on port 5432 (for storing data)  

After running `astro dev start`, both services were up. I could trigger the pipeline from the Airflow UI, and then connect to Postgres and run `SELECT *` to see the ingested records.  

---

## Challenge – Manual Triggers

Initially, I had to manually trigger the DAG each day to fetch the new APOD data. That wasn’t scalable if I wanted this to run daily without me checking in.  

---

## Cloud Deployment with Astronomer + AWS RDS

To automate it fully, I deployed the project on Astronomer Cloud, connected to an AWS RDS PostgreSQL instance.  

Here, the DAG was scheduled to run automatically every day.  

Now the pipeline ingests new data daily without manual triggers.  

---

## End Result

Today, even if I come back after two months, I can just connect to my Postgres database, run a query, and I’ll see all the APOD records from the past till today — because the DAG has been running daily on its own.  

---

## Deep Diving into the Technical Part

My DAG is written in Python using Airflow’s **TaskFlow API with task decorators**, which makes the code cleaner and dependencies easier to manage.  

The pipeline has four tasks:

1. **Create Table** → Using a `PostgresHook`, I first ensure the Postgres table exists. If it doesn’t, the task creates it.  
2. **Extract** → Then I fetch the Astronomy Picture of the Day from NASA’s API. This can be done with a `SimpleHttpOperator` or directly with `requests`. The response comes back as JSON.  
3. **Transform** → I clean and reshape that JSON, pulling only the fields I need like `title`, `explanation`, `date`, `media_type`, and `image URL`.  
4. **Load** → Finally, with another `PostgresHook`, I insert the cleaned data into the database.  

The flow is simple: **Create → Extract → Transform → Load**.  

Since it’s scheduled daily, Airflow automatically triggers it, and my Postgres database ends up with both **historical and fresh APOD records every single day**.  

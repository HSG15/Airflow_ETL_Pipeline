# 🚀 NASA APOD ETL Pipeline with Airflow, Docker, and AWS Deployment

This project is an end-to-end ETL pipeline that fetches data from NASA's Astronomy Picture of the Day (APOD) API, transforms it, and loads it into a PostgreSQL database. The project starts locally using Airflow and Docker, and is then deployed to the cloud using Astronomer and AWS.

---

## 📁 Project Setup (Local Development)

### 1. Clone or Create Project Folder

```bash
mkdir ETL_Airflow_Project && cd ETL_Airflow_Project
code .  # open in VS Code
```

### 2. Initialize Airflow Project

```bash
astro dev init
```

This sets up the basic Airflow and Docker environment with the correct file structure.

### 3. Create Your DAG

Create a file named `etl.py` inside the `dags/` folder.
Write your DAG to:

* Fetch APOD data using `requests`
* Transform relevant fields
* Create a Postgres table
* Load data into it

📚 [NASA APOD API](https://api.nasa.gov/)

### 4. Get API Key from NASA

* Visit [https://api.nasa.gov](https://api.nasa.gov)
* Sign up and get your **free API key**

### 5. Docker Compose Configuration

In your `docker-compose.yml`, define your Postgres service:

```yaml
services:
  postgres:
    image: postgres:13
    container_name: POSTGRES_DB
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: postgres
    ports:
      - "5432:5432"
    networks:
      - airflow_network

volumes:
  postgres_data:

networks:
  airflow_network:
    external: false
```

### 6. Start the Environment

```bash
astro dev start
```

### 7. Configure Airflow Connections

Navigate to [http://localhost:8080](http://localhost:8080) and go to **Admin > Connections**.

#### 🔗 Create Postgres Connection

| Field     | Value                    |
| --------- | ------------------------ |
| Conn ID   | `my_postgres_connection` |
| Conn Type | `Postgres`               |
| Host      | `postgres`               |
| Schema    | `postgres`               |
| Login     | `postgres`               |
| Password  | `postgres`               |
| Port      | `5432`                   |

#### 🌐 Create HTTP API Connection

| Field     | Value                           |
| --------- | ------------------------------- |
| Conn ID   | `nasa_api_connection`           |
| Conn Type | `HTTP`                          |
| Host      | `https://api.nasa.gov`          |
| Extra     | `{ "api_key": "YOUR_API_KEY" }` |

<img width="3358" height="930" alt="image" src="https://github.com/user-attachments/assets/d9129787-fb5c-4140-b6f9-9a543126d764" />

<img width="1674" height="666" alt="Screenshot 2025-07-11 at 8 26 31 AM" src="https://github.com/user-attachments/assets/70f7d111-c3b6-42ed-bb90-67596c024b2e" />

### 8. Verify Data in DB

Install [DBeaver](https://dbeaver.io/) and connect to Postgres:

* Host: `localhost`
* Port: `5432`
* User: `postgres`
* DB: `postgres`
* Password: `postgres`

You should now see your `nasa_apod_data` table populated.

<img width="1680" height="1050" alt="Screenshot 2025-07-11 at 8 25 23 AM" src="https://github.com/user-attachments/assets/2c0ced86-fa3a-4828-9b11-24a3df99a217" />

---

## ☁️ Deploying to the Cloud (AWS via Astronomer)

### 1. Create Astronomer Account

* Go to [https://www.astronomer.io](https://www.astronomer.io)
* Sign up and choose **AWS** as your cloud provider

### 2. Login via Astro CLI

```bash
astro login
```

### 3. Deploy to Cloud

```bash
astro deployment list  # get your deployment ID
astro deploy <deployment_id> -f
```

This deploys your code to Astronomer on AWS.

<img width="1680" height="1050" alt="Screenshot 2025-07-11 at 9 43 51 AM" src="https://github.com/user-attachments/assets/4b2fd3a4-d1ed-41eb-b1df-81fbd8bcdb6c" />

### 4. Create AWS RDS PostgreSQL

* Go to [AWS RDS Console](https://console.aws.amazon.com/rds/)
* Create a **PostgreSQL** database
* Make it publicly accessible if needed (security groups must allow port 5432)

### 5. Copy RDS Endpoint

Example: `database-1.cvg400akejc8.eu-north-1.rds.amazonaws.com`

### 6. Open Airflow on Astronomer Cloud

* After pushing your code with astro deploy:
* Go to your Astronomer Workspace > DAGs > Click "Open in Airflow"

<img width="1680" height="411" alt="Screenshot 2025-07-12 at 12 00 25 AM" src="https://github.com/user-attachments/assets/a611b3d0-e982-49d6-9a59-2d7c8c9e9473" />


### 7. Create Cloud Airflow Connections

In your deployed Astronomer Airflow UI:

#### Postgres Connection

| Field    | Value                    |
| -------- | ------------------------ |
| Conn ID  | `my_postgres_connection` |
| Host     | `<your-rds-endpoint>`    |
| Port     | `5432`                   |
| Schema   | `postgres`               |
| Login    | `your_rds_username`      |
| Password | `your_rds_password`      |

#### HTTP API Connection

Same as local setup:

* Conn ID: `nasa_api_connection`
* Conn Type: `HTTP`
* Host: `https://api.nasa.gov`
* Extra: `{ "api_key": "YOUR_API_KEY" }`

---

## ✅ Success! Your ETL is Live 🎉

| Step               | Description                            |
| ------------------ | -------------------------------------- |
| `create_table()`   | Ensures the Postgres table exists      |
| `extract_apod()`   | Pulls JSON data from NASA's APOD API   |
| `transform_apod()` | Extracts and structures key fields     |
| `load_data()`      | Inserts the cleaned data into Postgres |
| DAG                | Runs daily via the Airflow scheduler   |

Now your pipeline is fully automated and running in the cloud. 🌍🚀

---

## 🛠️ Useful Links

* [NASA API Docs](https://api.nasa.gov/)
* [Astronomer Docs](https://docs.astronomer.io/)
* [Airflow Official Docs](https://airflow.apache.org/docs/)
* [AWS RDS Setup Guide](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.html)
* [DBeaver DB Tool](https://dbeaver.io/)

---

## 🙏 Special Thanks

This project showcases the power of Airflow, Docker, and Astronomer for scalable data engineering. Thanks for checking it out!

---

» Made with ❤️ by  [Lucky](https://www.linkedin.com/in/hsg15/)

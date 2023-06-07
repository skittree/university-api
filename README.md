# University API

The following repository contains a university management schema and a FastAPI implementation of it. Created for a job position.

## Installation

### **Method 1: Docker (Recommended)**

This method allows for an easy installation of both the PostgreSQL database and API using Docker containers.

1. Make sure to have [**Docker**](https://www.docker.com) installed and running with **Compose** on your local machine before setup. Use Linux containers.

2. Clone the repository to a local machine:
```bash
git clone https://github.com/skittree/university-api.git
```

3. (Recommended) Edit the `.env` file in the root directory to store your own configuration parameters for the API for safety reasons:

```dotenv
PORT={your_api_port}
POSTGRES_USER={your_db_username}
POSTGRES_PASSWORD={your_db_password}
POSTGRES_SERVER={your_db_server}
POSTGRES_PORT={your_db_port}
POSTGRES_DB={your_db_name}
```

4. Run the script `compose.sh` to install the requirements and build the necessary Docker containers, images and volumes. The database tables are automatically initialized upon launch:

```bash
docker compose -f "docker-compose.yml" up -d --build
```

### **Method 2: Manual**

This method requires access to a pre-existing remote PostgreSQL database. The API will launch on your local machine.

1. Clone the repository to a local machine:
```bash
git clone https://github.com/skittree/university-api.git
```

2. Install the requirements in your virtual environment:
```bash
pip install -r requirements.txt
```

3. Edit the `.env` file in the root directory to match the credentials to access your PostgreSQL database:

```dotenv
PORT={your_api_port}
POSTGRES_USER={your_db_username}
POSTGRES_PASSWORD={your_db_password}
POSTGRES_SERVER={your_db_server}
POSTGRES_PORT={your_db_port}
POSTGRES_DB={your_db_name}
```
   
4. Launch the API app on port `8000` by running the following command:

```bash
gunicorn --bind 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker app.main:app
```

## Usage

To launch the documentation on a local machine that is running the API on default port `8000`, you can use the following link: http://localhost:8000/docs.

Similarly, using the default `.env` parameters, the DB connection link is `postgresql://localhost:5432/university`.
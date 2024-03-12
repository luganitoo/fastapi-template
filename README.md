# FastAPI ETL API template Documentation

This FastAPI application performs an ETL process retrieving data from a CSV file and loads it into a database.
It provides an API for various endpoints to query and retrieve vehicle-related data stored in a relational database.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
  - [Get VINs](#get-vins)
  - [Get Companies](#get-companies)
  - [Get Column Data by VIN](#get-column-data-by-vin)
  - [Get Last Updated Data by VIN](#get-last-updated-data-by-vin)
  - [Get All Data by VIN](#get-all-data-by-vin)
  - [Get Data from Time Window](#get-data-from-time-window)
  - [Get Statistics by VIN](#get-statistics-by-vin)
- [Docker Commands](#docker-commands)
- [Customize Configuration](#customize-configuration)
- [License](#license)

## Getting Started

Follow the steps below to set up and run the FastAPI application locally.

**IMPORTANT:** make sure your device's port 80 is free, and you have docker running.

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Running the Application

1. **Clone the repository to your local machine**:

   ```bash
   git clone https://github.com/luganitoo/fastapi-template.git
   ```

2. **Navigate to the project directory**:

   ```bash
   cd fastapi-template
   ```

3. **Rename .env.example to .env, or create your own .env:**

   Linux or Mac:
   ```bash
   cd src
   mv .env.example .env
   cd ..
   ```
   Windows:
    ```bash
   cd src
   ren .env.example .env
   cd ..
    ```
    
5. **To run tests, run the command below to create a test container:**

   ```bash
   docker-compose -f docker-compose.test.yaml run --rm test
   ```
   
5. **To run the app, build the Docker image and start the container:**

   ```bash
   docker-compose build
   docker-compose up
   ```

6. **Execute a GET request to the /load-data endpoint with the authentication token from your .env file. This action triggers the ETL process, loading the database.:**

   Substitute 'YOUR_SECRET_KEY_HERE' with your authentication token:
   ```bash
   curl -X GET http://localhost:80/load-data -H "Authorization: Bearer YOUR_SECRET_KEY_HERE"
   ```
   Or do it without exposing the Token:
   ```bash
   curl -X GET http://localhost:80/load-data -H "Authorization: Bearer $(grep SECRET_KEY src/.env | cut -d '=' -f2)"
   ```
   

7. **Access the FastAPI application at [http://localhost:80](http://localhost:80)**
   
**IMPORTANT**: It is mandatory that the SECRET_KEY token is sent in the Authorization Header to make the API calls. You can use curl, or any tool/extension of your choice to generate the requests. Otherwise you'll get a authentication error.

## API Endpoints

### Get VINs

- **Endpoint:** `/api/v1/vins`
- **Method:** `GET`
- **Description:** Retrieve a list of all VINs.

### Get Companies

- **Endpoint:** `/api/v1/companies`
- **Method:** `GET`
- **Description:** Retrieve a list of all unique companies.

### Get Column Data by VIN

- **Endpoint:** `/api/v1/data/{column}/{vin}`
- **Method:** `GET`
- **Description:** Retrieve the last updated data from a specific column for a given VIN.

### Get Last Updated Data by VIN

- **Endpoint:** `/api/v1/vehicle/{vin}/last`
- **Method:** `GET`
- **Description:** Retrieve the last updated data from all columns for a specific vehicle VIN.

### Get All Data by VIN

- **Endpoint:** `/api/v1/vehicle/{vin}`
- **Method:** `GET`
- **Description:** Retrieve all data entries for a specific vehicle VIN.

### Get Data from Time Window

- **Endpoint:** `/api/v1/vehicles/date-hour-range`
- **Method:** `GET`
- **Description:** Retrieve data entries within a specified time window, with optional data points filtering.

### Get Statistics by VIN

- **Endpoint:** `/api/v1/statistics/{vin}`
- **Method:** `GET`
- **Description:** Calculate basic statistics for a specific vehicle VIN.

## Docker Commands

- **Build the Docker image:**
  ```bash
  docker-compose build
  ```

- **Start the Docker container:**
  ```bash
  docker-compose up
  ```

- **Stop the Docker container:**
  ```bash
  docker-compose down
  ```

## Customize Configuration

- Modify the FastAPI application code in `api/main.py` as needed.
- Adjust the dependencies in `requirements.txt`.
- Customize the Dockerfile and `docker-compose.yml` as required.

## License

This project is licensed under the [MIT License](LICENSE.md).

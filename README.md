# Customer Interaction Analytics with MongoDB, Twilio, Datadog, Snowflake, and Docker

## Overview

This project simulates a customer support system using:

- **MongoDB**: Stores customer complaints
- **Twilio**: Sends SMS updates
- **Datadog**: Logs complaint events
- **Snowflake**: Stores aggregated complaint data
- **Docker**: Containers for easy deployment

## Tech Stack

- Python, Flask
- MongoDB
- Twilio API
- Datadog
- Snowflake
- Docker

## Prerequisites

Before running this project, ensure you have the following installed:

1. **Docker** – [Download and install Docker](https://www.docker.com/get-started).
2. **Docker Compose** – Comes pre-installed with Docker Desktop.
3. **WSL 2 (For Windows users)** – Required for running Linux-based containers in Docker.
4. **Python 3.12 or later** – If running locally without Docker.

## Setup

### **Building the Project from Scratch**

If you're setting up the project for the first time or after making changes to dependencies, follow these steps:

1. Clone this repository:

   ```sh
   git clone https://github.com/aleksgeorgi/customer_interactions_project.git
   ```

2. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

3. Build and start services using Docker:

   ```sh
   docker-compose up --build
   ```

### **Quick Start (For Existing Builds)**

If no dependencies or Docker configurations have changed, you can start the project quickly using:

```sh
   docker-compose up
```

### **Running Locally Without Docker**

If you prefer to run the project outside of Docker:

1. Start MongoDB manually (ensure it's running on `localhost:27017`).
2. Run the Flask API:
   ```sh
   python app.py
   ```

## API Endpoints

- **GET /complaints/<company>** → Returns complaints for a specific company
- **POST /complaints** → Adds a new complaint
- **PUT /complaints/<complaint_id>** → Updates an existing complaint by its ID

## Testing with cURL or PowerShell

You can interact with the API using either cURL (Unix-based) or PowerShell (Windows).

### **Fetch Complaints for a Company**

#### Using cURL:
```sh
curl "http://localhost:5000/complaints/MOHELA"
```

#### Using PowerShell:
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/complaints/MOHELA" -Method Get
```

### **Add a New Complaint**

#### Using cURL:
```sh
curl -X POST "http://localhost:5000/complaints" -H "Content-Type: application/json" -d '{"Company": "MOHELA", "Issue": "Billing error", "Description": "Unexpected charge on account"}'
```

#### Using PowerShell:
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/complaints" -Method Post -Headers @{"Content-Type"="application/json"} -Body '{"Company": "MOHELA", "Issue": "Billing error", "Description": "Unexpected charge on account"}'
```

### **Update a Complaint**

#### Using cURL:
```sh
curl -X PUT "http://localhost:5000/complaints/679c16f8cf4944fca50b01d0" -H "Content-Type: application/json" -d '{"Issue": "Updated Issue", "Description": "Updated Description"}'
```

#### Using PowerShell:
```powershell
$complaintId = "679c16f8cf4944fca50b01d0"  
$updateData = @{
    "Issue" = "Updated Issue"
    "Description" = "Updated Description"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/complaints/$complaintId" -Method Put -ContentType "application/json" -Body $updateData
```

### Notes

- Ensure your Flask application is running and accessible at `http://localhost:5000` before attempting these requests.
- Replace `MOHELA` and `679c16f8cf4944fca50b01d0` with the actual company name and complaint ID you wish to use.

## Future Improvements

- Add authentication
- Implement a frontend dashboard
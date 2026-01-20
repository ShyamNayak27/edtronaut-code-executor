# Edtronaut Live Code Execution Engine

This is a secure, reliable, and scalable backend system for executing user-submitted Python code in real-time. Built as part of the SWE Intern assignment for Edtronaut.

## 🚀 Tech Stack
- **Backend:** Python (FastAPI)
- **Task Queue:** Celery
- **Broker/Result Backend:** Redis
- **Database:** SQLite (SQLAlchemy)
- **Infrastructure:** Docker & Docker Compose

## 🛠️ Setup & Installation (One-Command Setup)
1. Ensure you have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
2. Clone the repository and navigate to the folder.
3. Run the following command:
   ```bash
   docker compose up --build
# Edtronaut: Live Code Execution Engine (Backend)

This repository contains the backend implementation for the **Live Code Execution** feature of the Edtronaut Job Simulation Platform. The system allows users to write, save, and execute Python code in a secure, asynchronous, and isolated environment.

---

## 🏗️ Architecture Overview

The system follows a **Producer-Consumer** architectural pattern to ensure high performance and reliability.

### 1. High-Level Diagram

```text
[ Client (Browser) ]
       |
       | (REST API / HTTP)
       v
[ FastAPI Web Server ] <----> [ SQLite Database ]
       |
       | (Enqueue Task)
       v
[ Redis Message Broker ]
       |
       | (Consume Task)
       v
[ Celery Worker ] ----------> [ Isolated Subprocess (Code Execution) ]
       |                               |
       +-------------------------------+
       | (Update Status & Result)
       v
[ SQLite Database ]
```
### 2. Component Explanation

* **FastAPI (Web Layer):** Handles incoming requests, validates data using **Pydantic**, and manages the lifecycle of code sessions.
* **Redis (Broker):** Acts as the "Waiting Room" for code execution tasks, ensuring the API remains responsive under heavy load.
* **Celery (Worker):** The background engine that retrieves tasks from Redis, executes the code, and updates the database.
* **SQLite (Persistence):** Stores code sessions and execution metadata.
* **Subprocess (Isolation):** Each execution is spawned as a separate OS process with a **strict 5-second timeout** to prevent infinite loops and resource exhaustion.

## 🚀 Setup Instructions

The system is fully dockerized for a "one-command" setup, fulfilling the infrastructure requirements of the assignment.

### Prerequisites
* **Docker Desktop** installed and running.

### Installation Steps
1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd edtronaut-code-executor
    ```
2.  **Start the system:**
    ```bash
    docker compose up --build
    ```
    *This command downloads Redis, builds the Python environment, and starts the API and Worker services simultaneously.*

3.  **Verify Startup:**
    The API will be available at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📡 API Documentation

### 1. Code Sessions
* **POST** `/code-sessions`
    * Creates a new session for a technical task.
    * **Payload:** `{"language": "python", "template_code": "string"}`
    * **Response:** `{"session_id": "uuid", "status": "ACTIVE"}`
* **PATCH** `/code-sessions/{session_id}`
    * Updates the session code (**Autosave**).
    * **Payload:** `{"source_code": "print('Hello World')"}`
    * **Response:** `{"session_id": "uuid", "status": "ACTIVE"}`

### 2. Execution
* **POST** `/code-sessions/{session_id}/run`
    * Submits the current code in the session for asynchronous execution.
    * **Response:** `{"execution_id": "uuid", "status": "QUEUED"}`
* **GET** `/executions/{execution_id}`
    * Polls for the result of a code run.
    * **Response:**
    ```json
    {
      "execution_id": "uuid",
      "status": "COMPLETED",
      "stdout": "Hello World\n",
      "stderr": "",
      "execution_time_ms": 120
    }
    ```
    * **States:** `QUEUED`, `RUNNING`, `COMPLETED`, `FAILED`, `TIMEOUT`.

---

## 🧠 Design Decisions & Trade-offs

| Decision | Reason |
| :--- | :--- |
| **Asynchronous Worker** | Running user code is "heavy." Using Celery/Redis prevents the API from blocking, allowing the platform to handle many concurrent users without lag. |
| **Subprocess vs exec()** | Using `exec()` in Python is a security risk. `subprocess.run()` isolates the execution and allows for strict timeout enforcement. |
| **SQLite (Trade-off)** | **Choice:** Used for simplicity and portability in this case study. **Trade-off:** In a high-traffic production environment, I would swap this for PostgreSQL. |
| **Polling (Trade-off)** | **Choice:** Used a GET endpoint for results. **Trade-off:** WebSockets would be a better choice for a "Real-time" feel with lower latency. |
| **Pydantic Schemas** | Used to ensure strict data validation before it ever touches the worker. |

---

## 🛠️ Future Improvements

* **Enhanced Sandboxing:** Implement **gVisor** or Linux Namespaces to completely isolate the worker's file system and network access.
* **Multi-Language Support:** Adding Java, C++, or JavaScript execution would simply require adding those compilers to the Dockerfile.
* **Real-time Feedback (WebSockets):** Implement WebSockets so the result is "pushed" to the learner the moment it finishes.
* **Advanced Observability:** Integrate **Prometheus** and **Grafana** to monitor average execution time and worker queue depth in real-time.
* **Code Linting:** Add a pre-execution check (like **Flake8**) to provide feedback before the learner runs the code.

---

## 💡 AI Usage Statement

In alignment with Edtronaut's guidelines, AI tools were utilized during this project to:
* Optimize **Docker multi-stage build** configurations.
* Design the **asynchronous task lifecycle**.
* Debug **cross-platform pathing issues** between Windows and Docker Linux containers.


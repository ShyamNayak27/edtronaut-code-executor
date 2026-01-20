# System Design Document: Live Code Execution Engine

This document outlines the architectural decisions, reliability strategies, and scalability considerations for the Edtronaut Live Code Execution backend.

---

## 1. Architecture Overview

### End-to-End Request Flow
The system manages the lifecycle of a coding task through five distinct stages:



1.  **Code Session Creation:** User initializes a task. The API creates a `CodeSession` record in SQLite with a unique `session_id` and a template code block.
2.  **Autosave Behavior:** As the user types, the frontend sends frequent `PATCH` requests to `/code-sessions/{id}`. This ensures the current state is persisted for crash recovery.
3.  **Execution Request:** When the user clicks "Run," a `POST` request is sent. The API creates an `Execution` record with a `QUEUED` status and returns an `execution_id` immediately.
4.  **Background Execution:** The API (Producer) pushes a message into **Redis**. A **Celery Worker** (Consumer) retrieves the task, writes the code to a temporary environment, and executes it via a restricted subprocess.
5.  **Result Polling:** The frontend periodically calls `GET /executions/{id}`. Once the worker finishes, it updates the database with `stdout`, `stderr`, and `execution_time_ms`.

### Queue-Based Execution Design
By utilizing **Redis** as a broker and **Celery** as the worker engine, the system decouples the "request" from the "work." 

> **Key Benefit:** Even if an execution takes 5 seconds, the API remains non-blocking and responsive to other users' autosaves while the worker handles the computational load.

---

## 2. Reliability & Data Model

### Execution Lifecycle & State Management
States are managed strictly in the `executions` table to ensure data integrity:

| State | Description |
| :--- | :--- |
| **QUEUED** | Task is in Redis waiting for an available worker. |
| **RUNNING** | Worker has initialized and started the subprocess. |
| **COMPLETED** | Code ran and exited with status 0. |
| **FAILED** | Code encountered a syntax error or runtime crash. |
| **TIMEOUT** | Code exceeded the 5-second safety limit. |

### Error Handling & Idempotency
* **Preventing Duplicate Runs:** Each run request generates a unique `execution_id`. Multiple clicks on "Run" result in separate execution tracks, preventing race conditions.
* **Retries:** For transient failures (e.g., database locks), Celery is configured with **exponential backoff**.
* **Safety Isolation:** Comprehensive `try-except` blocks capture OS-level errors and Python tracebacks, piping them into `stderr` to provide helpful feedback to the learner.

---

## 3. Scalability Considerations

### Handling Concurrency
* **FastAPI & Async:** The web server uses an `async/await` architecture, allowing it to handle thousands of concurrent I/O-bound autosave requests with minimal overhead.
* **Horizontal Scaling:** The worker layer is designed to scale horizontally. In a production environment, multiple Worker containers can be deployed across different nodes, all listening to the same Redis queue.

### Bottlenecks & Mitigations
* **SQLite Locking:** While sufficient for development, SQLite may struggle with high-frequency concurrent writes.
    * *Mitigation:* Swap for **PostgreSQL** in production.
* **Redis Memory:** High task volumes can consume significant memory.
    * *Mitigation:* Automated TTL (Time-To-Live) cleanup scripts for logs older than 24 hours.

---

## 4. Trade-offs

### Technology Choices
* **FastAPI vs. Flask:** FastAPI was chosen for native async support and automatic Swagger (OpenAPI) documentation, accelerating the development cycle.
* **Celery/Redis:** Chosen as the industry standard for Python background tasks. While a simple `ThreadPool` would be easier to set up, it lacks the persistence and retry logic required for a production-grade platform.

### Production Readiness Gaps
To transition this system to a live enterprise environment, the following would be implemented:
1.  **PostgreSQL Migration:** For enterprise-grade concurrency.
2.  **Enhanced Sandboxing:** Implement **gVisor** or **Nsjail** to isolate the worker's filesystem and network access completely.
3.  **Authentication:** JWT-based auth to ensure private access to code sessions.
4.  **WebSockets:** Replace polling with WebSockets for a lower-latency "instant" feedback feel.

---

## 👤 About the Developer

I am a **Sophomore BTECH Computer Science student specializing in Artificial Intelligence**. I am fluent in **C++, Python, JavaScript, and Java**, with a focus on building scalable backend architectures. My technical background includes **Machine Learning certifications from Stanford and Coursera**, and I am currently a **2026 Semester Abroad student at Ho Chi Minh City University of Technology (HCMUT), Vietnam**, where I am furthering my knowledge in AI integration and system design.
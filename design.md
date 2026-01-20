# System Design Decisions

## 1. Asynchronous Execution
Code execution is handled by a **Producer-Consumer** pattern. The API (Producer) pushes jobs to Redis, and a dedicated Worker (Consumer) executes them. This ensures that long-running or infinite-loop code submitted by users does not block the main API thread.

## 2. Safety & Security
- **Time Limits:** Enforced via `subprocess.run(timeout=5)`.
- **Isolation:** Each execution runs in a separate process within a Docker container, limiting access to the host machine.
- **Resource Protection:** The system is designed to handle high concurrency by scaling worker containers horizontally.

## 3. Trade-offs & Scaling
- **Database:** Used SQLite for simplicity in this case study. In production, I would move to **PostgreSQL** for better concurrent write handling.
- **State Management:** Polling (`GET /executions/{id}`) was chosen for its reliability and simplicity. For a more "live" feel, **WebSockets** could be implemented to push results instantly.
# CDC Pipeline

This project demonstrates a complete Change Data Capture (CDC) pipeline using PostgreSQL, Debezium, Redis, and a Python consumer. It captures row-level changes from a database table in real-time and streams them to a downstream service.

## Install Python and uv

To install Python on Linux or macOS, the recommended approach depends on your system and preferences. On Linux, the easiest method is using the system's package manager, such as `apt` on Ubuntu, to install Python 3 and related tools like `pip` and `venv`. On macOS, using Homebrew is often preferred for its ease of installation and future updates, though the official installer from python.org is also reliable.


To install uv for Python development, use the official standalone installer script. On macOS or Linux, run the following command in your terminal:

```javascript
curl -LsSf https://astral.sh/uv/install.sh | sh
```

If `curl` is not available, use `wget` instead:

```javascript
wget -qO- https://astral.sh/uv/install.sh | sh
```


uv can also be installed via PyPI using `pip`, `pipx`, Homebrew, or Cargo, depending on your system.


## Architecture

The pipeline is composed of two main parts: the `data-layer` and the `service-layer`.

### 1. Data Layer (`data-layer/`)

This layer is managed by Docker Compose and includes:

* **PostgreSQL**: The source database containing an `employee` table.
* **Debezium**: A CDC platform that connects to PostgreSQL. It monitors the `employee` table for any `INSERT`, `UPDATE`, or `DELETE` operations.
* **Redis**: A message broker. Debezium publishes the captured change events to a Redis Stream.

When this layer is active, any modification to the `employee` table is automatically captured and sent to the `cdc-server.test_schema.employee` Redis stream.

### 2. Service Layer (`service-layer/`)

This layer contains the downstream application that acts on the change events:

* **Python Consumer (**`consumer.py`): A Python script that connects to the Redis stream, reads the events published by Debezium, parses them, and logs the details of each database change to the console.
* **Python Inserter (**`insert_employees.py`): A utility script to populate the PostgreSQL database with sample data from a CSV file, which helps in testing the end-to-end flow of the CDC pipeline.

## How to Run the Pipeline

To see the pipeline in action, you will need two separate terminal windows.

### Step 1: Start the Data Layer

In your first terminal, navigate to the `data-layer` directory and start the infrastructure.

```bash
cd data-layer
docker compose up -d
```

### Step 2: Start the Event Consumer

In your second terminal, navigate to the `service-layer` directory and run the Python consumer. This will start listening for change events from the Redis stream.

```bash
cd service-layer
uv run python consumer.py
```

The consumer will first process any existing events in the stream (including the initial record from the database setup) and then wait for new ones.

### Step 3: Generate Database Changes

To test the pipeline, you can generate new events by running the employee insertion script from the `service-layer` directory.

```bash
uv run python insert_employees.py
```

As new records are inserted into the PostgreSQL database, you will see the corresponding `CREATE` events appear in the terminal where the consumer is running.
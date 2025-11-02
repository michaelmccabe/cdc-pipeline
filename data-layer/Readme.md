# Data Layer

The data layer contains the config for the database, the redis-stream event messaging and the debezium connector which sends events on data changes to the employee table

## Run and test

To run and test this setup, open a terminal at the data-layer folder.

### Run the Data Layer

```
docker compose up -d
```


### Check Stream Length in Redis

```
docker compose exec redis redis-cli XLEN cdc-server.test_schema.employee
```

The init sql adds a single entry to the employee table so this should give us

```
(integer) 1
```

This command runs the Redis CLI inside the "redis" container from Docker Compose to query the length of a specific stream key, "cdc-server.test_schema.employee". The XLEN command returns the number of entries (messages) in that Redis Stream, which stores CDC events from Debezium. For example, it might output "5" if there are five captured changes (like snapshots or inserts). It's a quick diagnostic tool to verify if events have been appended without reading the full content, helping confirm the pipeline is populating the stream.


Next, we test the CDC pipeline is configured correctly by adding an entry to the table and checking the stream entries.

### Add a row to the employee table

```
docker compose exec postgres psql -U postgres -d postgres -c "INSERT INTO test_schema.employee (firstname, lastname, email, age, salary) VALUES ('Frank', 'Future', 'frank@future.com', 45, 80000.00);"
```

This command executes a SQL INSERT statement inside a running PostgreSQL container named "postgres" from a Docker Compose setup. It connects as the user "postgres" to the "postgres" database and adds a new row to the "test_schema.employee" table with sample employee details: firstname "Frank", lastname "Future", email "frank@future.com", age 45, and salary 80000.00. The -c flag runs the query non-interactively, making it ideal for scripting or testing; it outputs "INSERT 0 1" if successful, confirming one row was added. This simulates a database change to trigger the CDC pipeline.

### Check Stream Length in Redis

```
docker compose exec redis redis-cli XLEN cdc-server.test_schema.employee
```

should now show

```
(integer) 2
```


### Reading All Entries from Redis Stream

```
docker compose exec redis redis-cli XRANGE cdc-server.test_schema.employee - +
```

This command uses the Redis CLI in the "redis" container to retrieve all historical entries from the "cdc-server.test_schema.employee" stream using XRANGE. The - (start) and + (end) arguments fetch every message from the beginning to the latest, outputting each as a key-value pair with IDs (e.g., timestamps) and payloads (JSON CDC events like inserts or updates). It's useful for inspecting the full event history, such as snapshot data or recent changes, and returns structured output for debugging or verification.



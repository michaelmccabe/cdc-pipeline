# Service Layer

The service layer contains the python service which will consume the messages from redis-stream and log them to the console.


It also has a script to add more entries to the table from a csv file.


## Initialise and Run the Consumer

To run and test this setup, open a terminal at the data-layer folder.

### Run Consumer

```javascript
uv run python consumer.py
```


You should see something like

```
2025-11-02 10:29:20,997 - WARNING - Stream check failed: no such key
2025-11-02 10:29:20,997 - INFO - Starting consumer for stream: cdc-server.test_schema.employee
2025-11-02 10:29:20,997 - INFO - Processing ALL entries from stream: cdc-server.test_schema.employee
2025-11-02 10:29:20,999 - INFO - Processed 0 total events.
2025-11-02 10:29:20,999 - INFO - Tailing new entries from ID: $
2025-11-02 10:29:21,508 - INFO - Event ID 1762079361507-0: op='r' | After:
{
  "id": 1,
  "firstname": "Jane",
  "lastname": "Doe",
  "email": "jane@doe.com",
  "age": 30,
  "salary": 50000.0
} | Before:
N/A
2025-11-02 10:29:21,508 - INFO -   -> CREATE: New employee (ID 1762079361507-0)
```

### Run Script to insert new employees

The insert_employees.py script consumes a CSV file and adds a list of new employees to the database. Open a new terminal and run the insert employees script


```
uv run python insert_employees.py

Inserted: Alice Johnson
Inserted: Bob Williams
Inserted: Carol Brown
Inserted: David Garcia
Inserted: Eve Miller
Successfully inserted 5 employees from employees.csv. Skipped 0 due to errors.
```



In the terminal running the consumer you should now see

```
2025-11-02 10:29:42,253 - INFO - Event ID 1762079382170-0: op='c' | After:
{
  "id": 2,
  "firstname": "Alice",
  "lastname": "Johnson",
  "email": "alice.johnson@example.com",
  "age": 32,
  "salary": 62000.45
} | Before:
N/A
2025-11-02 10:29:42,253 - INFO -   -> CREATE: New employee (ID 1762079382170-0)
2025-11-02 10:29:42,255 - INFO - Event ID 1762079382170-1: op='c' | After:
{
  "id": 3,
  "firstname": "Bob",
  "lastname": "Williams",
  "email": "bob.williams@example.com",
  "age": 45,
  "salary": 78000.12
} | Before:
N/A
2025-11-02 10:29:42,255 - INFO -   -> CREATE: New employee (ID 1762079382170-1)
2025-11-02 10:29:42,255 - INFO - Event ID 1762079382170-2: op='c' | After:
{
  "id": 4,
  "firstname": "Carol",
  "lastname": "Brown",
  "email": "carol.brown@example.com",
  "age": 29,
  "salary": 51000.78
} | Before:
N/A
2025-11-02 10:29:42,255 - INFO -   -> CREATE: New employee (ID 1762079382170-2)
2025-11-02 10:29:42,256 - INFO - Event ID 1762079382171-0: op='c' | After:
{
  "id": 5,
  "firstname": "David",
  "lastname": "Garcia",
  "email": "david.garcia@example.com",
  "age": 51,
  "salary": 92000.34
} | Before:
N/A
2025-11-02 10:29:42,256 - INFO -   -> CREATE: New employee (ID 1762079382171-0)
2025-11-02 10:29:42,256 - INFO - Event ID 1762079382171-1: op='c' | After:
{
  "id": 6,
  "firstname": "Eve",
  "lastname": "Miller",
  "email": "eve.miller@example.com",
  "age": 37,
  "salary": 68000.91
} | Before:
N/A
2025-11-02 10:29:42,256 - INFO -   -> CREATE: New employee (ID 1762079382171-1)

```



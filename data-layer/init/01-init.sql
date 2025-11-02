-- Enable replication role for user
ALTER USER postgres REPLICATION;

-- Create schema and table
CREATE SCHEMA IF NOT EXISTS test_schema;

CREATE TABLE IF NOT EXISTS test_schema.employee (
    id SERIAL PRIMARY KEY,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    age INTEGER NOT NULL,
    salary REAL
);

-- Insert initial data for testing
INSERT INTO test_schema.employee (firstname, lastname, email, age, salary)
VALUES ('Jane', 'Doe', 'jane@doe.com', 30, 50000.00);
BEGIN;
CREATE TABLE people (
    id SERIAL PRIMARY KEY NOT NULL,
    name TEXT
);
CREATE TABLE addresses (
    id SERIAL PRIMARY KEY NOT NULL,
    person INTEGER NOT NULL REFERENCES people(id),
    address TEXT NOT NULL
);
-- CREATE VIEW people_addresses AS
COMMIT;

psql -d postgres

CREATE DATABASE matzip_sns;

CREATE USER admin WITH PASSWORD 'admin';

ALTER ROLE admin SET client_encoding TO 'utf8';
ALTER ROLE admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE admin SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE matzip_sns TO admin;

\q

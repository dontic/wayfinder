-- Alter user roles
ALTER ROLE django SET client_encoding TO 'utf8';
ALTER ROLE django SET default_transaction_isolation TO 'read committed';
ALTER ROLE django SET timezone TO 'UTC';

-- Grant all privileges to the user
GRANT ALL PRIVILEGES ON DATABASE django TO django;

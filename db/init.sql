SELECT 'CREATE DATABASE exchanges_db'

WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'exchanges_db')
CREATE DATABASE finappaiohttp;
CREATE USER finapp_aiohttp PASSWORD 'finapp_http';
GRANT ALL PRIVILEGES ON DATABASE finappaiohttp TO finapp_aiohttp;
CREATE SCHEMA landing;
SET search_path TO landing;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA landing TO finapp_aiohttp;
GRANT ALL ON SCHEMA landing TO finapp_aiohttp;
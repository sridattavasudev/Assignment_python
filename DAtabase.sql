-- Database: NewDb

-- DROP DATABASE IF EXISTS "NewDb";

CREATE DATABASE "NewDb"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_India.1252'
    LC_CTYPE = 'English_India.1252'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;
	
	
	CREATE TABLE Public."stock_data" (
    date DATE,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    adj_close NUMERIC,
    volume NUMERIC
);

SELECT * FROM Public."stock_data";
COPY Public."stock_data" FROM 'C:\New folder (4)\data\AAPL.csv' DELIMITER ',' CSV HEADER;
COPY Public."stock_data" FROM 'C:\New folder (4)\data\HDB.csv' DELIMITER ',' CSV HEADER;
COPY Public."stock_data" FROM 'C:\New folder (4)\data\INRX.csv' DELIMITER ',' CSV HEADER;
COPY Public."stock_data" FROM 'C:\New folder (4)\data\JIOFINNS.csv' DELIMITER ',' CSV HEADER;
COPY Public."stock_data" FROM 'C:\New folder (4)\data\MARA.csv' DELIMITER ',' CSV HEADER;
COPY Public."stock_data" FROM 'C:\New folder (4)\data\TATAMOTORSNS.csv' DELIMITER ',' CSV HEADER;
COPY Public."stock_data" FROM 'C:\New folder (4)\data\TSLA.csv' DELIMITER ',' CSV HEADER;

create database postman_data;

use postman_data;

CREATE SCHEMA IF NOT EXISTS postman_data.public;

create table postman_data.public.product_final (name text, sku text, description text, primary key (sku));

CREATE or replace FILE FORMAT "POSTMAN_DATA"."PUBLIC".MYCSVFORMAT_1 COMPRESSION = 'AUTO' FIELD_DELIMITER = ',' RECORD_DELIMITER = '\n' SKIP_HEADER = 1 FIELD_OPTIONALLY_ENCLOSED_BY = '\042' TRIM_SPACE = FALSE ERROR_ON_COLUMN_COUNT_MISMATCH = TRUE ESCAPE = 'NONE' ESCAPE_UNENCLOSED_FIELD = '\134' DATE_FORMAT = 'AUTO' TIMESTAMP_FORMAT = 'AUTO' NULL_IF = ('\\N');

create or replace stage my_csv_ file_format = mycsvformat_1;

put file://C:/Users/rishi/Desktop/python_files/Posmantask/products.csv @my_csv_ auto_compress=true;

copy into TABLE_FINAL from @my_csv_/products.csv.gz file_format = (format_name = mycsvformat_1);

create table Aggregate_final as select name, count(*) as Num_Of_Products from postman_data.public.product_final group by name;
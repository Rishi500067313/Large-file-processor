use postman_data;

CREATE TABLE temp_update_table (name text, sku text, description text);

copy into temp_update_table from @my_csv_/products.csv.gz file_format = (format_name = mycsvformat_1) on_error = 'skip_file';

update product_final set product_final.description = temp_update_table.description from temp_update_table where temp_update_table.sku = product_final.sku;
  
drop table temp_update_table;
use postman_data;

update table_2 set table_2.description = temp_update_table.description from temp_update_table where temp_update_table.sku = table_2.sku;
  
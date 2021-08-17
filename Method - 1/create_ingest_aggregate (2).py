#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import pymysql
from sqlalchemy import create_engine

data = pd.read_csv('products.csv')

class Sql_code:
    
    @staticmethod
    def connect_to_mysql():
        
        conn_dic = {'user': 'root', 'password': 'password', 'host': '127.0.0.1', 'database': 'postman_data','raise_on_warnings': True}
        connect_alchemy = "mysql+pymysql://%s:%s@%s/%s" % (conn_dic['user'], conn_dic['password'], conn_dic['host'], conn_dic['database'])
        print('Connecting to the MySQL')
        engine = create_engine(connect_alchemy)
        print("Connection successfull")
        return engine

    @staticmethod
    def create_table(engine):
        engine.execute("CREATE DATABASE IF NOT EXISTS postman_data;")
        print("postman_data database is created successfully")  
        engine.execute("DROP TABLE IF EXISTS product_final;")
        sql = '''CREATE TABLE product_final(name varchar(50) NOT NULL, sku varchar(200) NOT NULL, description varchar(350) NOT NULL)'''
        engine.execute(sql)
        print("post table is created successfully")  
   
    @staticmethod
    def ingest_data(engine, datafrm, table):

        datafrm.to_sql(table, con=engine, index=False, if_exists='append',chunksize = 1000)
        print("Data inserted using to_sql() done successfully")
    
    @staticmethod
    def update(engine, datafrm):
        engine.execute("DROP TABLE IF EXISTS temp_update_table;")
        engine.execute("CREATE TABLE temp_update_table (name varchar(50), sku VARCHAR(255), description VARCHAR(300) NOT NULL);")
        print("table created successfully")
        datafrm.to_sql('temp_update_table', con=engine, index=False, if_exists='append',chunksize = 1000)
        print("Data inserted successfully")
        sql = '''UPDATE product_final INNER JOIN temp_update_table on temp_update_table.sku = product_final.sku SET product_final.name = temp_update_table.name SET product_final.description = temp_update_table.description;'''
        engine.execute(sql);
        engine.execute("DROP TABLE temp_update_table;")
        print("Updation of table is successfull")
    
def main():
    
    obj = Sql_code()
    engine = obj.connect_to_mysql()
    obj.create_table(engine)
    obj.ingest_data(engine, data, 'product_final')

    query_pk = ('ALTER TABLE postman_data.product_final ADD CONSTRAINT PK_sku PRIMARY KEY (sku, description);')
    engine.execute(query_pk)
    print("Altered post table for Primary key successfully")

    query = ('create table aggregate_Final as select name, count(*) as Num_Of_Products from product_final group by name;')
    engine.execute(query)
    print("Aggregate table with name and Num_Of_Products is created successfully")
    
    argument = input()
    print("Press: 1 to update existing table product_final")
    print("Press: 0 to exit")
    if(argument == 1):
        engine = obj.connect_to_mysql()
        obj.update(engine, data)
    else:
        print("exit")

if __name__ == '__main__':
    main()


# Large-File-Processor

Aim is to build a system which is able to handle long running processes in a distributed fashion.

### Problem Statement

We need to be able to import products from a CSV file and into a database. There are half a million product details to be imported into the database.After the import, we will run an aggregate query to give us no. of products with the same name.

Points to achieve
   1. Your code should follow concept of OOPS
   2. Support for regular non-blocking parallel ingestion of the given file into a table. Consider thinking about the scale of what should happen if the file is to be processed in       2 mins.
   3. Support for updating existing products in the table based on `sku` as the primary key.
   4. All product details are to be ingested into a single table
   5. An aggregated table on above rows with `name` and `no. of products` as the columns
  

### Method - 1: By Using Python and MySQL

This the most think about method to do any work. In this method I used Python with MySQL as the database. 

  #### Steps to run the code:
  
  The code is configured with a docker container. The docker image can be accessed from here: https://drive.google.com/file/d/1a2R2ak8NcIgVCJMpipbDGJOgo3Cg5Dfb/view?usp=sharing 
  
  1. Assuming you have docker installed...
  2. Firstly you have to download the docker image.
  3. Then you need to place the python code, docker image and products.csv in a same folder.
  4. We need to load this downloaded file first to get a docker image as it is not downloaded from hub.docker.com
     
     `docker load --input postman_dockerimage`
     
  5. Then to run the container that will execute our code use:
     
     `docker run -it --name postmanos -e MYSQL_ROOT_PASSWORD=password -e MYSQL_USER=root -e MYSQL_PASSWORD=password -e MYSQL_DATABASE=postman_data -v <location_of_csv>:<any_location_in_container> postman_dockerimage`
     
     NOTE: *You need to specify in this command where the products.csv is located and then mount it to any location in docker. The location where which choose in docker will have to be updated in the python code also.*
     
     ![Capture9](https://user-images.githubusercontent.com/50805925/128622624-573abe98-d773-4e44-a273-8e1c7b7e47a8.PNG) 
     
     Specify the location here...

  
  #### Details of all the tables and their schema:
   
   1. There are three tables here that are being created:
      - Product_Final
      - Aggregate_Final
      - Temp_Update_Table
      
   2. The first table `Product_Final` has three columns: name, sku and description where *sku* is the Primary Key & *description* is the composite key having 500000 rows.
      
      ![Capture1](https://user-images.githubusercontent.com/50805925/128563574-e31210db-bede-4861-93fb-0bd73b71d9ae.PNG)
      
      To create this table the command is:
      
      `CREATE TABLE product_final(name varchar(50) NOT NULL, sku varchar(200) NOT NULL, description varchar(350) NOT NULL)`
      
      After ingestion of data the table is altered with this command:
      
      `ALTER TABLE postman_data.product_final ADD CONSTRAINT PK_sku PRIMARY KEY (sku, description);`
      
      Few rows from this table after ingestion of products.csv:
      
      ![Capture3](https://user-images.githubusercontent.com/50805925/128563908-faf43c65-c133-4369-8520-b74d57f04f6f.PNG)
      
   3. The second table `Aggregate_Final` has three columns: name and Num_of_products having 222024 rows.
   
      ![Capture2](https://user-images.githubusercontent.com/50805925/128564389-f81b88c6-2f0c-46fd-9c10-cfdd43695080.PNG)
       
      To create this table the command is:
      
      `create table aggregate_Final as select name, count(*) as Num_Of_Products from product_final group by name;`
       
      Few rows from this table after aggreation query (CTAS) of product_final:
      
      ![Capture4](https://user-images.githubusercontent.com/50805925/128564591-ad7366c7-0cfa-46e3-bdb5-bc6a161ea6ff.PNG)
       
   4. The third table is only created when we need to update the table product_final. It is a **temporary table** which is dropped after its use.
      
      We just ingest the new csv into this table and run a update query.
      
      
      
      To create this table the command is:
      
      `CREATE TABLE temp_update_table (name varchar(50), sku VARCHAR(255), description VARCHAR(300) NOT NULL);`
      
      After creating table the new csv is ingested into the table. Then Update the products_final table using this command:
      
      `UPDATE product_final INNER JOIN temp_update_table on temp_update_table.sku = product_final.sku SET product_final.name = temp_update_table.name;`
   
   
  #### Points achieved by this method:
   
   By using python with MySQL 4 out of 5 points were completely fullfilled.
   
   1. The python code fully uses the OOPs concept in the implementation of the task.
   2. The code does the creation & ingestion of table in about 15 seconds while the updation task involves join with temporary table so it takes about 8 minutes to complete. 
   3. The code has the functionality to execute the update on the product_final table. Therefore there is updation support for the table.
   4. All the product details are ingested directly to a single table *product_final*.
   5. The aggregate table was also created by using CTAS command on product_final. 
  
  #### Points not achieved by this method:
  
   The updation takes about 8 minutes to complete due to join so the second point somewhat fails in this case.
   
  #### Improving if given more days:
  
  In this mysql method for updation join is used which becomes very expensive command to run as it takes 8 minutes of time while doing update in snowfalke jsut took 15 seconds.
  To improve this we can use mysql query caching and avoid the inner join by using evaluate and select kind of queries.
  
  Apart from the two methods I did here if given more time, I would have done it with few more methods to achieve this task either by using Apache NiFi and Apache Spark with delta table.
  
  
  
### Method - 2: By Using Snowflake
  
This method is all about usage of snowflake data warehouse. In this method I used the snowflake with SQL to achieve all the expected tasks.
  #### Steps to run the code:
   1. Firstly we need a snowflake account to get started.
      You can sign up using this link to get your snowflake account: https://signup.snowflake.com/.
      
      Then after signing in you will be taken to link of this type: https://az30528.east-us-2.azure.snowflakecomputing.com/console where *az30528.east-us-2.azure* will be your           accountname, and you have to specify your username and password at the time of signing up.
      
   2. Then there are two ways to execute the SQL scripts.
      - First one is by using *snowsql CLI*. (This one is preferred)
      - Second by the worksheet in the console by importing the scripts.
   3. To use snowsql first you need to install it. You can refer this to download and install it: https://docs.snowflake.com/en/user-guide/snowsql-install-config.html.
   4. After it's installation follow these steps:
      - Open the command prompt.
      - Use command `snowsql` to verify installtion. 
        ![Capture](https://user-images.githubusercontent.com/50805925/128549407-5f500484-6acc-4b7c-8baa-46f900f22769.PNG) 
        [Ignore the log error :-)]
      - Now You can directly run the first script Script_to_ingest_data.sql by using this command.
      
        To execute a SQL script while connecting to Snowflake:
        
        `snowsql -a az30528.east-us-2.azure -u rishi -f C://Downloads/Script_to_ingest_data.sql` 
        
        `snowsql -a az30528.east-us-2.azure -u rishi -f C://Downloads/Script_to_update_data.sql` 
        
        *Edit your accountname, username & path* After running this command firstly it will ask for your password after which the script will be executed.
        
        To run a SQL script after connecting to Snowflake
         
        `rishi#> !source Script_to_ingest_data.sql`
      
   5. The second way will involve the usage of UI of snowflake:
      - Go to your console and create an new worksheet.
      
        ![Capture 1](https://user-images.githubusercontent.com/50805925/128551116-8892cfa6-e3ac-4f59-80a8-5e9e333f7d59.PNG)
        
      - Now import the script.
      
        ![Capture 2](https://user-images.githubusercontent.com/50805925/128551447-d027cd89-a342-4f00-9590-6adf11928cd6.PNG)
        
      - Now after importing the script you can run all the commands in sequence to get the result but the command number 11 will still have to be run on the snowsql CLI.
        
        ![Capture 4](https://user-images.githubusercontent.com/50805925/128551840-2d20bbde-ab3d-44cf-9b31-f3cef7982680.PNG)
        
      - Same thing is to be done with the both the scripts.
  
  #### Details of all the tables and their schema:
  
   1. There are three tables here that are being created:
      - Product_Final
      - Aggregate_Final
      - Temp_Update_Table
   
   2. The first table `Product_Final` has three columns: name, sku and description where *sku* is the Primary Key having 500000 rows.
   
      ![Capture 5](https://user-images.githubusercontent.com/50805925/128553810-8a39c883-d941-404d-bee7-2b29ccf48123.PNG)
      
      To create this table the command is:
      
      `create table postman_data.public.product_final (name text, sku text, description text, primary key (sku));`
      
      Few rows from this table after ingestion of products.csv:
      
      ![Capture 7](https://user-images.githubusercontent.com/50805925/128554920-fb0862ce-7434-459e-95b9-52914f271b05.PNG)
    
   3. The second table `Aggregate_Final` has three columns: name and Num_of_products having 222024 rows.
   
      ![Capture 6](https://user-images.githubusercontent.com/50805925/128554254-4afcf920-4471-4645-8ccf-aac6eed39b16.PNG)
      
      To create this table the command is:
      
      `create table Aggregate_final as select name, count(*) as Num_Of_Products from postman_data.public.product_final group by name;`
      
      Few rows from this table after aggreation query (CTAS) of product_final:
      
      ![Capture 8](https://user-images.githubusercontent.com/50805925/128555020-06276125-af42-4167-9f00-22f879526d53.PNG)
      
   4. The third table is only created when we need to update the table product_final. It is a **temporary table** which is dropped after its use.
      
      We just ingest the new csv into this table and run a update query.
      
      ![Capture 9](https://user-images.githubusercontent.com/50805925/128555664-70438599-ad1d-4a46-ad5b-aafb0d35ae92.PNG)
      
      To create this table the command is:
      
      `create table temp_update_table (name text, sku text, description text);`
      
      After creating ingest the new csv into the table. Then Update the products_final table using this command:
      
      `update product_final set product_final.description = temp_update_table.description from temp_update_table where temp_update_table.sku = product_final.sku;`
      
  #### Points achieved by this method:
   
   By using the snowflake all the 5 out of 5 points were completely fullfilled.
   
   1. As it is a sql script having sql command only, so there is no point and no way of using OOPs concept.
   2. As snowflake is a cloud based data warehousing product. So the analysis and processing is extremely fast on it. the whole operation including update also takes near about 1 minute.
   3. The script *Script_to_Update.sql* is the script which will be executed to update the product_final table. Therefore there is updation support for the table.
   4. All the product details are ingested directly to a single table *product_final*.
   5. The aggregate table was also created by using CTAS command on product_final.
  
  #### Points not achieved by this method:
  
   Everything was achieved using this method. 
  
  

   


  


        
    


      
      
      
      
      
      
      
      
      
      

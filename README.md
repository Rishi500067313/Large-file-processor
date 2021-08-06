# Large-File-Processor

Aim is to build a system which is able to handle long running processes in a distributed fashion.

### Problem statement

We need to be able to import products from a CSV file and into a database. There are half a million product details to be imported into the database.After the import, we will run an aggregate query to give us no. of products with the same name.

Points to achieve
   1. Your code should follow concept of OOPS
   2. Support for regular non-blocking parallel ingestion of the given file into a table. Consider thinking about the scale of what should happen if the file is to be processed in       2 mins.
   3. Support for updating existing products in the table based on `sku` as the primary key.
   4. All product details are to be ingested into a single table
   5. An aggregated table on above rows with `name` and `no. of products` as the columns

### Method - 1: By Using Python and MySQL




### Method - 2: By Using Snowflake

This method is all about usage of snowflake data warehouse. In this method I used the snowflake with SQL to achieve all the expected tasks.
Steps to run the code:
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
      - 


        
    


      
      
      
      
      
      
      
      
      
      

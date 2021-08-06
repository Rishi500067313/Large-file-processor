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



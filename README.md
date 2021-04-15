# Vend-Customer-To-Shopify-Identifier

The identification process starts by extracting the first name and last name of a customer from Vend data source and see if the combination exists in a Shopify customer record. 

If a Vend customer does not exist in Shopify customers database, we add the entire customer info json object into an array, which will be returned at the end of execution for identification process.

Data source for Vend customers: A JSON file obtained from Vend API 2.0 (avoid CSV exports as there's a limit of 1000 customers per CSV export, not ideal for large datasets)

Data source for Shopify customers: A CSV file exported from Shopify store admin that includes all customers data

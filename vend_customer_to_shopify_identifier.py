# Author: Mingyang Li 

# This program identifies which customers from Vend are not in Shopify store customers database.

# The identification process starts by extracting the first name and last name of a customer  
# from Vend data source and see if the combination exists in a Shopify customer record. 

# If a Vend customer does not exist in Shopify customers database, we add the entire customer info
# json object into an array, which will be returned at the end of execution for identification process.

# Data source for Vend customers: A JSON file obtained from Vend API 2.0 
# (avoid CSV exports as there's a limit of 1000 customers per CSV export, not ideal for large datasets)

# Data source for Shopify customers: A CSV file exported from Shopify store admin that includes all customers data

import json

json_file = json.load(open("./vend/customers/customers.json", "r", encoding="utf-8"))

class Vend_Customer_To_Shopify_Identifier:
    def __init__(self, vend_filename, shopify_filename):
        self.__vend_filename = vend_filename
        self.__shopify_filename = shopify_filename
        self.__shopify_customers = []
        self.__vend_customers = []

    # opening shopify customers CSV file in this case
    def populate_shopify_customers(self, filename):
        import csv
        with open(filename, encoding='utf-8', mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            # collecting customers that have complete value sets for full name and email
            for line in csv_reader:
                first_name = line[0]
                last_name = line[1]
                # start from line 2, only append rows that have both firs name, last name and emails
                if first_name != 'first_name' and last_name != 'last_name':
                    if first_name != None and last_name != None:
                        self.__shopify_customers.append(
                            [first_name, last_name])
        return "self.__shopify_customers array is created"

    # opening vend customers json file in this case
    def populate_vend_customers(self, filename):
        import json
        f = open(filename, "rb")
        allCustomers = json.load(f)
        f.close()
        allCustomers = allCustomers["data"]
        for i in range(len(allCustomers)):
            customer = allCustomers[i]
            customer_code = customer["customer_code"]
            first_name = customer["first_name"]
            last_name = customer["last_name"]
            email = customer["email"]
            # only append rows that have both firs name, last name and emails
            if first_name != None and last_name != None and email != None:
                self.__vend_customers.append(
                    [first_name, last_name, email, customer_code])
        return "self.__vend_customers array is created"

    def get_vend_customers_not_in_shopify(self):
        filtered_customers = []
        for shopify_customer in self.__shopify_customers:
            for vend_customer in self.__vend_customers:
                pass
        import json
        f = open(filename, "rb")
        allCustomers = json.load(f)
        f.close()
        allCustomers = allCustomers["data"]
        return filtered_customers
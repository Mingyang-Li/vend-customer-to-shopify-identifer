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
import csv

class Vend_Customer_To_Shopify_Identifier:
    def __init__(self, vend_filename, shopify_filename, difference_filename):
        self.__vend_filename = vend_filename
        self.__shopify_filename = shopify_filename
        self.__difference_filename = difference_filename
        self.__shopify_customers = []
        self.__vend_customers = []
        self.__filtered_customers = []

    # opening shopify customers CSV file in this case
    def populate_shopify_customers(self):
        with open(self.__shopify_filename, encoding='utf-8', mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            # collecting customers that have complete value sets for full name and email
            for line in csv_reader:
                first_name = line[0]
                last_name = line[1]
                # start from line 2, only append rows that have both firs name, last name and emails
                if first_name != 'First Name' and last_name != 'Last Name':
                    if first_name != None and last_name != None:
                        if first_name.lower() == "customer" and last_name.lower() == "customer":
                            self.__shopify_customers.append({
                                "first_name": first_name,
                                "last_name": last_name
                            })
        return "self.__shopify_customers array is created"

    # opening vend customers json file in this case
    def populate_vend_customers(self):
        f = open(self.__vend_filename, "rb")
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
                self.__vend_customers.append({
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "customer_code": customer_code
                })
        return "self.__vend_customers array is created"

    def get_shopify_customers(self):
        return self.__shopify_customers
    
    def get_vend_customers(self):
        return self.__vend_customers

    def filter_difference(self):
        shopify_customers =[]
        for shopify_customer in self.__shopify_customers:
            if shopify_customer["first_name"] == "Customer" and shopify_customer["last_name"] =="Customer":
                shopify_combined_str = shopify_customer["first_name"].lower() + shopify_customer["last_name"].lower()
                shopify_customers.append((shopify_combined_str))

        for vend_customer in self.__vend_customers:
            vend_combined_str = vend_customer["first_name"].lower() + vend_customer["last_name"].lower()
            if vend_combined_str not in shopify_customers:
                self.__filtered_customers.append(vend_customer["customer_code"])
    
    def get_filtered_customers(self):
        return self.__filtered_customers

    def create_vend_customers_file_for_shopify_import(self):
        # Get difference 
        difference = self.get_filtered_customers()

        # Get original vend customer detail from original vend customers file
        vend_file = open(self.__vend_filename, "rb")
        allCustomers = json.load(vend_file)
        allCustomers = allCustomers["data"]
        vend_file.close()

        # Open a blank csv
        with open(self.__difference_filename, 'w') as file_to_write:
            field_names = [k for k in allCustomers[0].keys()]

            writer = csv.DictWriter(file_to_write, fieldnames=field_names)

            writer.writeheader()

            # Write the whole customer detail onto it row by row
            for i in range(len(allCustomers)):
                customer = allCustomers[i]
                if customer["customer_code"] in difference:
                    row = {}
                    for key in customer:
                        row[key] = customer[key]
                    # print(row)
                    try:
                        writer.writerow(row)
                    except Exception as e:
                        print(e)
        file_to_write.close()
        print("Done")
            

    def clear_difference_file(self):
        pass

if __name__ == "__main__":
    identification = Vend_Customer_To_Shopify_Identifier("customers.json", "shopify_customers.csv", "difference.csv")
    identification.populate_shopify_customers()
    identification.populate_vend_customers()
    identification.filter_difference()
    identification.create_vend_customers_file_for_shopify_import()


import requests
from decouple import config


def get_token():
    # URL to which you are sending the POST request
    url = config('TOKEN_ENDPOINT')

    # Body parameters (can be a dictionary)
    data = {
        "grant_type": config('GRANT_TYPE'),
        "client_id": config('CLIENT_ID'),
        "client_secret": config('CLIENT_SECRET'),
        "refresh_token": config('REFRESH_TOKEN'),
    }

    # Send POST request with body parameters
    response = requests.post(url, data=data)

    # Check if the request was successful
    if response.status_code == 200:
        # print("Request was successful.")
        return response.json()["access_token"]
    else:
        print("Failed to make request. Status code:", response.status_code)


def set_product(token, id, itemlookupcode, description, price, subdescription1, subdescription2):
    # URL to which you are sending the POST request
    url = config('PRODUCT_ENDPOINT')

    # Body parameters (can be a dictionary)
    payload = {
        "data": [
            {
                "Product_Name": f"{description}",
                "Product_Code": f"{itemlookupcode}",
                "Item_ID": f"{id}",
                "itemlookupcode": f"{itemlookupcode}",
                "SubDescription1": f"{subdescription1}",
                "SubDescription2": f"{subdescription2}",
                "Unit_Price": f"{price}",
                "Entity": 'Carina Wear',
            }
        ]
    }

    # Headers to be included in the request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Zoho-oauthtoken {token}",  # Example authorization token
    }

    # Send POST request with body parameters
    response = requests.post(url, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code in [200, 201]:  # Zoho CRM may return 200 or 201 for successful creation
        print("Request was successful.")
        response_data = response.json()

        # Extract the record ID from the response
        try:
            record_id = response_data['data'][0]['details']['id']
            print("Record ID:", record_id)
            return record_id
        except (KeyError, IndexError) as e:
            print("Could not retrieve Record ID. Error:", e)
            print("Response Data:", response_data)

    else:
        print("Failed to make request. Status code:", response.status_code)
        print("Response:", response.json())
        if response.status_code == 400:
            response = response.json()
            return response['data'][0]['details']['duplicate_record']['id']


def set_customer(token, firstname, lastname, email, phone, customerid, enrollmentdate):
    # URL to which you are sending the POST request
    url = config('CUSTOMER_ENDPOINT')

    # Body parameters (can be a dictionary)
    payload = {
        "data": [
            {
                "Last_Name": f"{lastname}",
                "First_Name": f"{firstname}",
                "Email": f"{email}",
                "Phone": f"{phone}",
                "CustomerID": f"{customerid}",
                "enrollmentdate": f"{enrollmentdate}",
                "Entity": 'Carina Wear',
            }
        ]
    }

    print(payload)

    # Headers to be included in the request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Zoho-oauthtoken {token}",  # Example authorization token
    }

    # Send POST request with body parameters
    response = requests.post(url, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code in [200, 201]:  # Zoho CRM may return 200 or 201 for successful creation
        print("Request was successful.")
        response_data = response.json()

        # Extract the record ID from the response
        try:
            record_id = response_data['data'][0]['details']['id']
            print("Record ID:", record_id)
            return record_id
        except (KeyError, IndexError) as e:
            print("Could not retrieve Record ID. Error:", e)
            print("Response Data:", response_data)
    else:
        print("Failed to make request. Status code:", response.status_code)
        response_data = response.json()
        print("Response:", response_data)

        # Handle duplicate data error
        if response.status_code == 202 and response_data['data'][0]['code'] == 'DUPLICATE_DATA':
            duplicate_crm_id = response_data['data'][0]['details']['id']
            print(f"Duplicate detected. CRM ID: {duplicate_crm_id}")
            return duplicate_crm_id

        # Raise an exception for other errors
        raise Exception(f"Error syncing customer: {response_data}")

    # # Check if the request was successful
    # if response.status_code == 201:
    #     print("Request was successful.")
    #     return response.json()
    # else:
    #     print(response.json())
    #     print("Failed to make request. Status code:", response.status_code)


# def set_transaction():
#     # URL to which you are sending the POST request
#     url = config('TRANSACTION_ENDPOINT')

#     # Body parameters (can be a dictionary)
#     payload = {
#     "data": [
#         {
#             "Layout":{
#                 "id":"6568963000000091023"
#             },

#             "Lead_Source": "Employee Referral",
#             "Stage": "Closed Won",
#             "Last_Name": "test script",
#             "First_Name": "script test",
#             "Email": "abdelrahman.eldafrawy@carinawear.com",
#             "Amount": "5000",
#             "Branch": "Maadi",
#             "Sales_Person": "Test Sales",
#             "Deal_Type": "Sell",
#             "Deal_Name":"Test Deal",
#             "Closing_Date":"2025-02-01"
#         }
#     ]
# }

#     # Headers to be included in the request
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Zoho-oauthtoken {get_token()}",  # Example authorization token
#     }

#     # Send POST request with body parameters
#     response = requests.post(url, json=payload, headers=headers)

#     # Check if the request was successful
#     if response.status_code == 201:
#         print("Request was successful.")
#         return response.json()
#     else:
#         print(response.json())
#         print("Failed to make request. Status code:", response.status_code)


# def set_order():
#     # First, get the customer record ID
#     customer_id = "6568963000006266002"  # Replace with the actual customer ID

#     if not customer_id:
#         print("Failed to retrieve customer ID.")
#         return

#     # URL for creating an order in the Orders module
#     url = config('ORDER_ENDPOINT')

#     # Body parameters for the order
#     payload = {
#         "data": [
#             {
#                 "Subject": "New Customer Order",
#                 "Contact_Name": {   # This might also be Customer_Name or Account_Name, check your CRM fields
#                     "id": customer_id  # Link the order to the customer
#                 },
#                 "Order_Status": "Processing",
#                 "Grand_Total": 850.00,
#                 "Subform1": [
#                     {
#                         "Product_Name": {
#                             "id": "6568963000005775550"  # Use the product's record ID
#                         },
#                         "Quantity": 2,
#                         "Rate": 799.00
#                     }
#                 ],
#                 "Deal_Name":"Sales 2",
#                 "Order_Date": "2025-03-01",
#                 "Billing_City": "Maadi",
#                 "Billing_State": "Cairo",
#                 "Billing_Country": "Egypt"
#             }
#         ]
#     }

#     # Headers for the request
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Zoho-oauthtoken {get_token()}"
#     }

#     # Send POST request to create the order
#     response = requests.post(url, json=payload, headers=headers)

#     # Check if the request was successful
#     if response.status_code in [200, 201]:
#         print("Order was successfully created.")
#         response_data = response.json()

#         # Extract the order ID from the response
#         try:
#             order_id = response_data['data'][0]['details']['id']
#             print("Order ID:", order_id)
#             return order_id
#         except (KeyError, IndexError) as e:
#             print("Could not retrieve Order ID. Error:", e)
#             print("Response Data:", response_data)
#     else:
#         print("Failed to create Order. Status code:", response.status_code)
#         print("Response:", response.json())


def set_sales_order(token, order_id, customer_id, store_id, store_name, transaction_time, total, transaction_number,
                    tenders, store_type, cashierid, entries,FP):
    # First, get the customer record ID
    # customer_id = "6568963000006266002"  # Replace with the actual customer ID

    if not customer_id:
        print("Failed to retrieve customer ID.")
        return

    items_list = []
    for entry in entries:
        item = {
            "Product_Name": {
                "id": f"{entry.item_id}",  # Use the product's record ID
            },
            "Quantity": entry.quantity,
            "List_Price": entry.unit_price,
            "Discount": entry.discount,
        }
        items_list.append(item)

    # URL for creating a sales order
    url = config('SALES_ORDER_ENDPOINT')

    # Body parameters for the sales order
    payload = {
        "data": [
            {
                "Subject": f"Order ID: {order_id}",
                "Contact_Name": {
                    "id": f"{customer_id}"  # Link the sales order to the customer
                },
                "Customer_No": f"{customer_id}",
                "Transaction_Number": f"{transaction_number}",
                "Order_Status": "Approved",
                "Store_ID": f"{store_name}-{store_id}",
                "Sales_Person": f"{cashierid}",
                "Order_Total_Amount": f"{total}",
                "Order_Category": f"{store_type}",  # "OnlineStore" or "Walk In"
                "Account_Name": f"{store_type}",  # "OnlineStore" or "Walk In"
                "Tender": f"{tenders}",
                "Ordered_Items": items_list,
                "Due_Date": f"{transaction_time}",
                "Entity": 'Carina Wear',
                "Sales_Rep_Number": f"{FP}",
                # "Billing_City": "Maadi",
                # "Billing_State": "Cairo",
                # "Billing_Country": "Egypt"
            }
        ]
    }

    # Headers for the request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Zoho-oauthtoken {token}"
    }

    # Send POST request to create the sales order
    response = requests.post(url, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code in [200, 201]:
        print("Sales Order was successfully created.")
        response_data = response.json()
        print(response_data)
        # Extract the sales order ID from the response
        try:
            sales_order_id = response_data['data'][0]['details']['id']
            print("Sales Order ID:", sales_order_id)
            return sales_order_id
        except (KeyError, IndexError) as e:
            print("Could not retrieve Sales Order ID. Error:", e)
            print("Response Data:", response_data)
    else:
        print("Failed to create Sales Order. Status code:", response.status_code)
        response_data = response.json()
        print("Response:", response_data)

        # Handle invalid token or unauthorized error
        if response.status_code == 401 or response_data.get("code") == "INVALID_TOKEN":
            raise Exception("INVALID_TOKEN: The provided token is invalid or expired.")

        # Raise an exception for other errors
        raise Exception(f"Error creating sales order: {response_data}")


def get_product_id_by_lookup(itemlookupcode):
    # URL to search for a product by name
    url = f"https://www.zohoapis.com/crm/v2/Products/search?criteria=(itemlookupcode:equals:{itemlookupcode})"

    # Headers for the request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Zoho-oauthtoken {get_token()}"
    }

    # Send GET request to search for the product
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        print("Product search was successful.")
        response_data = response.json()

        # Extract the product ID from the response
        try:
            product_id = response_data['data'][0]['id']
            print("Product ID:", product_id)
            return product_id
        except (KeyError, IndexError) as e:
            print("Could not retrieve Product ID. Error:", e)
            print("Response Data:", response_data)
    else:
        print("Failed to search for Product. Status code:", response.status_code)
        print("Response:", response.json())



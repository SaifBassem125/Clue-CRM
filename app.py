import time
from endpoints import get_token, set_customer, set_sales_order, get_product_id_by_lookup, set_product
from crud import fetch_new_customers, fetch_new_products, add_product_mapping, add_customer_mapping, \
    fetch_new_transaction, get_customer_mapping_rms_id, fetch_transaction_entries, add_transaction_mapping
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import requests

HEARTBEAT_URL = "https://hc-ping.com/f1b70f60-3961-4e8e-b477-c3210fdb19af"


def send_heartbeat():
    try:
        requests.get(HEARTBEAT_URL, timeout=10,verify=False)
        print("Heartbeat sent successfully")
    except Exception as e:
        print("Heartbeat failed:", e)

# def refresh_token():
#     print("Refreshing token...")
#     new_token = get_token()  # Assuming `get_token` fetches a new token
#     print("Token refreshed.")
#     return new_token

def send_mail(subject, body, receivers):
    sender_email = "saif.basem@carinawear.com"
    password = "ykhu xxfo bobv ftrm"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = ", ".join(receivers)  # 👈 multiple emails here
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Email failed: {e}")



def product_sync():
    token = get_token()
    products = fetch_new_products()
    print(len(products))

    for product in products:
        print(f"Syncing: {product.id}")

        sku = product.itemlookupcode
        parts = sku.split('-')
        try:
            color = parts[1]
            size = '-'.join(parts[2:])
            new_description = f"{product.description} - {color} - {size}"
        except IndexError:
            color = ''
            size = ''
            new_description = f"{product.description}"

        try:
            record_id = set_product(token, product.id, product.itemlookupcode, new_description, product.price,
                                    product.subdescription1,
                                    product.subdescription2)
        except Exception as e:
            print(f"Error syncing product {product.id}: {e}")
            continue

        add_product_mapping(record_id, product.id)


def customer_sync():
    token = get_token()
    customers = fetch_new_customers()
    print(len(customers))
    for customer in customers:
        print(f"Syncing: {customer.id}")
        accountopened = customer.accountopened.strftime('%Y-%m-%d')
        lastname = customer.lastname if customer.lastname.strip() not in (None, '') else '.'
        # record_id = set_customer(token, customer.firstname, lastname, customer.emailaddress, customer.PhoneNumber, customer.id, accountopened)
        # add_customer_mapping(record_id, customer.id)
        phonenumber= ""
        if '01' in customer.PhoneNumber[:2]:
            phonenumber = f"+2{customer.PhoneNumber}"
        else:
            phonenumber=f"+{customer.PhoneNumber}"
        try:
            record_id = set_customer(token, customer.firstname, lastname, customer.emailaddress, phonenumber,
                                     customer.id, accountopened)
            add_customer_mapping(record_id, customer.id)
        except Exception as e:
            response = str(e)  # Convert the exception to a string to parse the response
            if "INVALID_TOKEN" in response:
                print("Token expired. Refreshing token...")
                token = get_token()  # Refresh the token once
                try:
                    # Retry the request with the new token
                    record_id = set_customer(token, customer.firstname, lastname, customer.emailaddress,
                                             customer.PhoneNumber, customer.id, accountopened)
                    add_customer_mapping(record_id, customer.id)
                except Exception as retry_error:
                    print(f"Error retrying customer sync for {customer.id}: {retry_error}")
                    break  # Exit the loop if retry fails
            else:
                print(f"Error syncing customer {customer.id}: {e}")


def transaction_sync():
    token = get_token()
    transactions = fetch_new_transaction()
    print(len(transactions))
    for transaction in transactions:
        print(f"Syncing: {transaction.id} - {transaction.transactionnumber} - {transaction.FP} ")
        customer_id = transaction.customerid
        # customer_mapping = get_customer_mapping_rms_id(customer)
        # if customer_mapping:
        #     customer_id = customer_mapping.crm_id
        #     print("mapping found")
        # else:
        #     print("mapping not found")
        #     continue
        order_id = transaction.id
        store_id = transaction.storeid
        store_name = transaction.storename
        transaction_time = transaction.transactiontime.strftime('%Y-%m-%d')
        total = transaction.total
        transaction_number = f"{transaction.transactionnumber}-{transaction.storeid}"
        tenders = transaction.tenders
        store_type = transaction.storetype
        cashierid = transaction.cashierid
        FP = transaction.FP

        entries = fetch_transaction_entries(transaction.transactionnumber, transaction.storeid)

        try:
            record_id = set_sales_order(token, order_id, customer_id, store_id, store_name, transaction_time, total,
                                        transaction_number, tenders, store_type, cashierid,entries,FP)
            add_transaction_mapping(record_id, order_id)

        except Exception as e:
            response = str(e)

            if 'INVALID_TOKEN' in response:
                print("Token expired. Refreshing token...")
                token = get_token()  # Refresh the token once
                try:
                    record_id = set_sales_order(token, order_id, customer_id, store_id, store_name, transaction_time,
                                                total, transaction_number, tenders, store_type, cashierid,entries,FP)
                    add_transaction_mapping(record_id, order_id)
                except Exception as retry_error:
                    print(f"Error retrying Transaction sync for {transaction.id}: {retry_error}")
                    break  # Exit the loop if retry fails
                else:
                    print(f"Error syncing transaction {transaction.id}")
                    continue


def main():
    product_sync()
    time.sleep(10)
    customer_sync()
    time.sleep(10)
    transaction_sync()
    send_mail(
        subject="Sync Completed Successfully Carina CRM Data",
        body="All sync tasks finished successfully Carina CRM Data.",
        receivers=[
            "khaled.abdelfatah@carinawear.com",
            "saif.basem@carinawear.com"
        ]
    )
    send_heartbeat()




main()

############################
# customer_id = set_customer()
# sales_order_id = set_sales_order()
# print(sales_order_id)


# order_id = set_sales_order()
# product_id = get_product_id_by_lookup("56447-50-10-12")
# print(set_product())

# Record id =6568963000006266002
# fetch_new_customers()



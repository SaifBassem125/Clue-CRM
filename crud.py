from sqlalchemy.orm import Session
from models import Customer, Transaction, Store, Product, ProductMapping, CustomerMapping, TransactionEntry, \
    TransactionMapping
from sqlalchemy import func
from database import get_session_sql_server, get_session_mapping
from datetime import datetime, timedelta


### CUSTOMERS INTEGRATION

# def get_new_customers(session: Session):
#      # Calculate yesterday's date
#     yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')

#     # Query the database using SQLAlchemy ORM
#     query = session.query(Customer).join(Transaction, Customer.id == Transaction.customerid) \
#         .join(Store, Transaction.storeid == Store.id) \
#         .filter(Store.zip.in_(['Carina Stores']) | (Store.id == '277'), Store.Inactive == 0) \
#         .filter(Transaction.transactiontime >= '2025-04-01') \
#         .filter(Customer.accountopened >= '2025-04-01') \
#         .filter(Transaction.total > 0) \
#         .filter(Customer.PhoneNumber != '') \
#         .filter(func.length(Customer.PhoneNumber) == 11) \
#         .distinct()

#     # Print the query
#     print(str(query))

#     # Execute the query
#     new_customers = query.all()

#      # Filter out products that already exist in rms_ids
#     #new_customers = [customer for customer in new_customers if customer.id not in customerids]

#     return new_customers

# def get_customer_mapping(session: Session):
#     # Query the database using SQLAlchemy ORM
#     customer_mapping = session.query(CustomerMapping).all()

#     return customer_mapping

def get_customer_mapping_rms_id(customer_id: int):
    with get_session_mapping() as session:
        try:
            customer_mapping = session.query(CustomerMapping).filter(CustomerMapping.rms_id == customer_id).all()
            if customer_mapping:
                return customer_mapping[0]
            else:
                return None
        except Exception as e:
            print(f"Error fetching customer mapping: {e}")
            return None


def add_customer_mapping(crm_id: int, rms_id: int):
    with get_session_mapping() as session:
        try:
            new_mapping = CustomerMapping(crm_id=crm_id, rms_id=rms_id)
            session.add(new_mapping)
            session.commit()
            print("Mapping Saved.")
        except:
            print("Something Went Wrong.")

        # To call this function and get the results


def fetch_new_customers():
    with get_session_sql_server() as session:  # Using context manager for session management
        new_customers = session.query(Customer).all()

    # with get_session_mapping() as session:  # Using context manager for session management
    #     customers_mapping = get_customer_mapping(session)
    #     mapping_ids = [customer.rms_id for customer in customers_mapping]

    # customers_to_create = [customer for customer in new_customers if customer.id not in mapping_ids]

    # print(f'Found {len(new_customers)} new customers')
    # print(f'Found {len(customers_mapping)} existing customers')
    # print(f'Found {len(customers_to_create)} customers to be created')

    return new_customers


### PRODUCTS INTEGRATION

# def get_new_products(session: Session):
#     # Define the date threshold
#     date_threshold = '2025-01-01'

#     # Query the database using SQLAlchemy ORM
#     new_products = session.query(Product) \
#         .filter(Product.datecreated > date_threshold) \
#         .all()

#     # Filter out products that already exist in rms_ids
#     # new_products = [product for product in new_products if product.id not in product_ids]

#     return new_products


# def get_product_mapping(session: Session):
#     # Query the database using SQLAlchemy ORM
#     product_mapping = session.query(ProductMapping).all()

#     return product_mapping


def add_product_mapping(crm_id: int, rms_id: int):
    with get_session_mapping() as session:
        try:
            new_mapping = ProductMapping(crm_id=crm_id, rms_id=rms_id)
            session.add(new_mapping)
            session.commit()
            print("Mapping Saved.")
        except:
            print("Something Went Wrong.")

        # OLD FETCH FUNCTION BEFORE THE MERGE


# def fetch_new_products():
#     with get_session_sql_server() as session:  # Using context manager for session management
#         new_products = get_new_products(session)

#     with get_session_postgres() as session:  # Using context manager for session management
#         products_mapping = get_product_mapping(session)
#         mapping_ids = [product.rms_id for product in products_mapping]

#     product_to_create = [product for product in new_products if product.id not in mapping_ids]

#     # print(f'Found {len(new_products)} new products')
#     # print(f'Found {len(products_mapping)} existing products')
#     # print(f'Found {len(product_to_create)} products to be created')

#     return product_to_create


def fetch_new_products():
    with get_session_sql_server() as session:  # Using context manager for session management
        new_products = session.query(Product).all()

    # print(f'Found {len(new_products)} new products')
    # print(f'Found {len(products_mapping)} existing products')
    # print(f'Found {len(product_to_create)} products to be created')

    return new_products


### TRANSACTION INTEGRATION

def fetch_new_transaction():
    print("Inside fetch_new_transaction")

    with get_session_sql_server() as session:
        print("Session opened")

        transactions = session.query(Transaction).all()

        print("Query executed")

    print("Returning data")
    return transactions


def add_transaction_mapping(crm_id: int, rms_id: int):
    with get_session_mapping() as session:
        try:
            new_mapping = TransactionMapping(crm_id=crm_id, rms_id=rms_id)
            session.add(new_mapping)
            session.commit()
            print("Mapping Saved.")
        except Exception as e:
            print(f"Something Went Wrong:{e}.")


def fetch_transaction_entries(transaction_number, store_id):
    with get_session_sql_server() as session:
        transaction_entries = session.query(TransactionEntry) \
            .filter(TransactionEntry.transactionnumber == transaction_number) \
            .filter(TransactionEntry.storeid == store_id) \
            .all()

    return transaction_entries


if __name__ == "__main__":
    print("START")

    transactions = fetch_new_transaction()

    print("DONE")

    for transaction in transactions:
        print(transaction.__dict__)
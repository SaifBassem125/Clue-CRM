from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime, Float, Numeric, BigInteger
from sqlalchemy.orm import relationship
from database import Base  # Import the base from database.py


class Customer(Base):
    __tablename__ = 'crm_customers'

    id = Column(Integer, primary_key=True)
    PhoneNumber = Column(String(50))
    firstname = Column(String(50))
    lastname = Column(String(50))
    accountopened = Column(DateTime)
    emailaddress = Column(String(100))

    # Define the relationship back to Transaction
    # transactions = relationship('Transaction', back_populates='customer')

    def __init__(self, customerid, mobilenumber, firstname, lastname):
        self.id = customerid
        self.PhoneNumber = mobilenumber
        self.firstname = firstname
        self.lastname = lastname


class CustomerMapping(Base):
    __tablename__ = 'customer_mapping'

    id = Column(Integer, primary_key=True)
    crm_id = Column(BigInteger)
    rms_id = Column(Numeric)

    def __init__(self, crm_id, rms_id):
        self.crm_id = crm_id
        self.rms_id = rms_id


class Product(Base):
    __tablename__ = 'crm_products'

    id = Column(Integer, primary_key=True)
    itemlookupcode = Column(String(50))
    description = Column(String(100))
    price = Column(Float)
    subdescription1 = Column(String(100))
    subdescription2 = Column(String(100))
    datecreated = Column(DateTime)

    def __init__(self, id, itemlookupcode, description, price, subdescription1, subdescription2, datecreated):
        self.id = id
        self.itemlookupcode = itemlookupcode
        self.description = description
        self.price = price
        self.subdescription1 = subdescription1
        self.subdescription2 = subdescription2
        self.datecreated = datecreated

    def __repr__(self):
        return f'Product {self.itemlookupcode} - {self.description}'


class ProductMapping(Base):
    __tablename__ = 'product_mapping'

    id = Column(Integer, primary_key=True)
    crm_id = Column(BigInteger)
    rms_id = Column(Numeric)

    def __init__(self, crm_id, rms_id):
        self.crm_id = crm_id
        self.rms_id = rms_id


class Transaction(Base):
    __tablename__ = 'crm_transactions'
    id = Column(Integer, primary_key=True)
    customerid = Column(Integer)
    transactionnumber = Column(String(100))
    storeid = Column(Integer)
    storename = Column(String(100))
    total = Column(Float)
    storetype = Column(String(50))
    tenders = Column(String(150))
    transactiontime = Column(DateTime)
    cashierid = Column(String(100))
    FP = Column(String(100))

    def __init__(self, id, customerid, transactionnumber, storeid, storename,
                 total, storetype, tenders, transaction_date, cashierid,FP):
        self.id = id
        self.customerid = customerid
        self.transactionnumber = transactionnumber
        self.storeid = storeid
        self.storename = storename
        self.total = total
        self.storetype = storetype
        self.tenders = tenders
        self.transaction_date = transaction_date
        self.cashierid = cashierid
        self.FP = FP

    def __repr__(self):
        return f'Transaction {self.transactionnumber} - {self.storename} - {self.tenders}'


class TransactionMapping(Base):
    __tablename__ = 'transaction_mapping'

    id = Column(Integer, primary_key=True)
    crm_id = Column(BigInteger)
    rms_id = Column(Numeric)

    def __init__(self, crm_id, rms_id):
        self.crm_id = crm_id
        self.rms_id = rms_id


class TransactionEntry(Base):
    __tablename__ = 'crm_transaction_entry'
    id = Column(Integer, primary_key=True)
    transactionnumber = Column(String(100))
    storeid = Column(Integer)
    item_id = Column(Numeric)
    quantity = Column(Integer)
    unit_price = Column(Float)
    discount = Column(Float)

    # itemlookupcode = Column(String(50))

    def __init__(self, id, transactionnumber, storeid, item_id, quantity, unit_price, discount, itemlookupcode):
        self.id = id
        self.transactionnumber = transactionnumber
        self.item_id = item_id
        self.storeid = storeid
        self.quantity = quantity
        self.unit_price = unit_price
        self.discount = discount
        # self.itemlookupcode = itemlookupcode

    def __repr__(self):
        return f'TransactionEntry: {self.item_id} - {self.quantity} - {self.unit_price}'
    # class TransactionEntry(Base):


#     __tablename__ = 'transactionentry'

#     transaction_number = Column(String(50), ForeignKey('transaction.transaction_number'))  # Link by transaction_number
#     qty = Column(Integer)
#     description = Column(String(255))

#     transaction = relationship('Transaction', back_populates='entries')  # Relationship back to Transaction

#     def __init__(self, transaction_number, qty, description):
#         self.transaction_number = transaction_number
#         self.qty = qty
#         self.description = description

class Store(Base):
    __tablename__ = 'store'

    id = Column(Integer, primary_key=True)
    zip = Column(String(50))
    Inactive = Column(Integer)


class LoyaltyCustomer(Base):
    __tablename__ = 'loyalty_customers'

    customerid = Column(Integer, ForeignKey('customer.id'), primary_key=True)


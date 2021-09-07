from sqlalchemy import Column, Integer, String, ForeignKey, Table, create_engine, asc, desc, func, and_
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select

Base = declarative_base()



savat = Table(
    "savat",
    Base.metadata,
    Column("customer_id", Integer, ForeignKey("customer.customer_id")),
    Column("product_id", Integer, ForeignKey("product.product_id")),
    Column("amount", Integer),
)


class Customer(Base):
    __tablename__ = "customer"
    customer_id = Column(Integer, primary_key=True)
    username = Column(String)
    phone = Column(String)
    language = Column(String(250))
    products = relationship(
        "Product", secondary=savat, back_populates="customers"
    )
    time = Column(String, nullable=True)
    comment = Column(String, nullable=True)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    def __repr__(self):
        return f"{self.username}"

class Product(Base):
    __tablename__ = "product"
    product_id = Column(Integer, primary_key=True)
    title = Column(String(250))
    description = Column(String(250))
    photo_id = Column(String(250)) 
    price = Column(String(250))
    customers = relationship(
        "Customer", secondary=savat, back_populates="products"
    )
    
    def __repr__(self):
        return self.title


class Organization(Base):
    __tablename__ = 'organization'
    title = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    # address = Column(String(250)) 
    phone_number = Column(String(250)) 



engine = create_engine('postgresql://postgres:sindarov03@localhost:5432/postgres')


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

# create a Session
session = Session()


customer = Customer(username="Murodbek", phone="+998727440", language="🇺🇿O'zbekcha", time="12:00 21.09.2021 da", comment="Bu shunchaki test", longitude="1212", latitude="2115")
session.add(customer)
session.commit()
# product = Product(title="Product title3", description="Product description3", price="322000", photo_id="photo_id3")
# customer = session.query(Customer).filter(Customer.customer_id == 1914622728).first() # Customer(customer_id=759631, username="Murodbek", phone="+998938727265", language="🇺🇿O'zbekcha",) #    
# customer.username = "Asadbek"

# product =session.query(Product).filter(Product.title == "Контрактубекс® 20 г гель для лечения рубцов и шрамов").first()   # Product(title="Контрактубекс® 20 г", description="эффект. ....", price="100000",photo_id="some photo_id again") 
# print(product.description)
# session.delete(product)
# session.commit()
# customer.products.remove(product)
# session.commit()
# print(product in customer.products)
# amount = int(input())

# if product in customer.products:
#     customer.products.remove(product)
#     session.commit()
# customer_savat = savat.insert().values(customer_id=customer.customer_id, product_id=product.product_id, amount=amount)



# customer.products.remove(product)
# session.commit()
# session.execute(customer_savat)
# customer.products.clear()
# session.commit()
# products = [(p.title, p.description) for p in customer.products]
# print(customer.products)
# for t in products:
#         print(t)    

# customer_savat = savat.insert().values(customer_id=customer.customer_id, product_id=product.product_id, amount=6)
# customer.products.remove(product)
# customer.products.remove(product)
# customer.products.remove(product)
# savat_del = savat.delete().where(savat.c.customer_id==759631, savat.c.product_id==product.product_id)
# session.delete(product)
# session.execute(customer_savat)
# session.commit()
# l = savat.filter(savat.c.customer_id==759631, savat.c.product_id==product.product_id)
# print(l)
# products = customer.savat
# products.remove(product)
# savat = savat.delete().where(savat.c.customer_id==customer.customer_id, savat.c.product_id==product.product_id)
# savat = savat.insert().values(customer_id=customer.customer_id,product_id=product.product_id, amount=5)
# print(customer.products)
# print(product)
# s = select([savat, Customer]).filter(savat.c.customer_id == customer.customer_id)
# results = session.execute(s)
# total_price = 0
# r = session.query(savat, Customer).filter(Customer.customer_id==customer.customer_id, savat.c.customer_id == customer.customer_id).all()
# for row in r:
#     print(row.amount)
#     print(row.product_id)
#     product = session.query(Product).filter(Product.product_id==row.product_id).first()
#     print(f"{row.Customer.username} {product.title}ni {row.amount} ta sotib oldi. ")
#     print(f"{row.amount} x {product.price} = {int(row.amount)*int(product.price)}")
#     total_price += int(row.amount)*int(product.price)
# print("Total price : %s" %total_price)    
# print(results.first())
# for row in results:
    # print(f"{row.amount} x {row.Product.price} = {int(row.amount) * int(row.Product.price)}")
    # total_price += int(row.amount) * int(row.Product.price)
    # print(row)
# print(f"Total price : {total_price}")    
    # print(row.customer_id)
    # print(row.product_id)
    # print(row.amount)
    # print(row.Customer)
    
# print(products)
# print(savat)
# session.add(customer)
# session.execute(savat)
# session.commit()

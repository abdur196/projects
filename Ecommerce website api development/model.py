from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pyodbc
from sqlalchemy import ForeignKey


# SQLAlchemy base
Base = declarative_base()

# Database URL for Windows Authentication
DATABASE_URL = (
    "mssql+pyodbc:///?"
    "driver=ODBC+Driver+18+for+SQL+Server&"
    "server=KILLSHOT\\ABDUR&"
    "database=ecommerce&"
    "trusted_connection=yes&"
    "encrypt=no"
)




# Create SQLAlchemy engine with the Windows Authentication connection string
engine = create_engine(DATABASE_URL)

# Session maker to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)   # ✅ Indexed with defined length
    price = Column(Float)
    category = Column(String(100))           # Recommended: add length


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))  # ✅ fixed
    total_amount = Column(Float)
    sale_date = Column(Date)


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))  # ✅ fixed
    quantity_change = Column(Integer)
    quantity = Column(Integer)

# Create tables in the database (if they don't exist)
Base.metadata.create_all(bind=engine)


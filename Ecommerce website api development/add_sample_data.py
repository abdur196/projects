from datetime import date
from sqlalchemy.orm import Session
from model import engine, SessionLocal, Product, Sale, Inventory  # adjust import based on your file structure

def add_sample_data():
    db: Session = SessionLocal()
    try:
        # Add sample products
        product1 = Product(name="Laptop", price=999.99, category="Electronics")
        product2 = Product(name="Smartphone", price=499.99, category="Electronics")
        product3 = Product(name="Coffee Mug", price=9.99, category="Kitchen")

        db.add_all([product1, product2, product3])
        db.commit()

        # Refresh to get generated IDs
        db.refresh(product1)
        db.refresh(product2)
        db.refresh(product3)

        # Add sample sales
        sale1 = Sale(product_id=product1.id, total_amount=999.99, sale_date=date(2025, 5, 1))
        sale2 = Sale(product_id=product2.id, total_amount=999.98, sale_date=date(2025, 5, 2))  # 2 sales of smartphone
        sale3 = Sale(product_id=product2.id, total_amount=499.99, sale_date=date(2025, 5, 3))
        sale4 = Sale(product_id=product3.id, total_amount=9.99, sale_date=date(2025, 5, 3))

        db.add_all([sale1, sale2, sale3, sale4])
        db.commit()

        # Add sample inventory
        inventory1 = Inventory(product_id=product1.id, quantity_change=10, quantity=10)
        inventory2 = Inventory(product_id=product2.id, quantity_change=20, quantity=20)
        inventory3 = Inventory(product_id=product3.id, quantity_change=50, quantity=50)

        db.add_all([inventory1, inventory2, inventory3])
        db.commit()

        print("Sample data added successfully.")

    except Exception as e:
        db.rollback()
        print(f"Error adding sample data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_sample_data()

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from model import Product, Sale, Inventory, get_db
from datetime import datetime
from sqlalchemy import func, cast, Date,text


app = FastAPI()

# Sales Status Endpoints
@app.get("/sales")
async def get_sales_by_date_range(start_date: str, end_date: str, db: Session = Depends(get_db)):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        sales = db.query(Sale).filter(Sale.sale_date >= start, Sale.sale_date <= end).all()
        if not sales:
            raise HTTPException(status_code=404, detail="No sales found for the given date range")
        return sales
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/revenue")
async def get_revenue_by_period(period: str, db: Session = Depends(get_db)):
    try:
        if period == "daily":
            revenue = (
                db.query(
                    cast(Sale.sale_date, Date).label("date"),
                    func.sum(Sale.total_amount).label("total_revenue")
                )
                .group_by(cast(Sale.sale_date, Date))
                .order_by(cast(Sale.sale_date, Date))
                .all()
            )
            result = [{"date": r.date.isoformat(), "total_revenue": r.total_revenue} for r in revenue]

        elif period == "weekly":
            revenue = (
                db.query(
                    text("DATEPART(wk, sales.sale_date) AS week"),
                    func.sum(Sale.total_amount).label("total_revenue")
                )
                .select_from(Sale)
                .group_by(text("DATEPART(wk, sales.sale_date)"))
                .order_by(text("DATEPART(wk, sales.sale_date)"))
                .all()
            )
            result = [{"week": r[0], "total_revenue": r[1]} for r in revenue]

        elif period == "monthly":
            revenue = (
                db.query(
                    func.month(Sale.sale_date).label("month"),
                    func.sum(Sale.total_amount).label("total_revenue")
                )
                .group_by(func.month(Sale.sale_date))
                .order_by(func.month(Sale.sale_date))
                .all()
            )
            result = [{"month": r.month, "total_revenue": r.total_revenue} for r in revenue]

        elif period == "annually":
            revenue = (
                db.query(
                    func.year(Sale.sale_date).label("year"),
                    func.sum(Sale.total_amount).label("total_revenue")
                )
                .group_by(func.year(Sale.sale_date))
                .order_by(func.year(Sale.sale_date))
                .all()
            )
            result = [{"year": r.year, "total_revenue": r.total_revenue} for r in revenue]

        else:
            raise HTTPException(status_code=400, detail="Invalid period. Choose from 'daily', 'weekly', 'monthly', or 'annually'.")

        if not result:
            raise HTTPException(status_code=404, detail="No revenue data found for the selected period.")

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
@app.get("/sales/product/{product_id}")
async def get_sales_by_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    sales = (
        db.query(
            Sale.product_id,
            func.sum(Sale.total_amount).label("total_sales")
        )
        .filter(Sale.product_id == product_id)
        .group_by(Sale.product_id)
        .first()
    )

    total_sales = sales.total_sales if sales else 0
    return {
        "product_id": product.id,
        "product_name": product.name,
        "total_sales": total_sales
    }

# Inventory Management Endpoints
@app.get("/inventory")
async def get_inventory(db: Session = Depends(get_db)):
    # Calculate current stock by summing quantity_change from Inventory for each product
    inventory_data = (
        db.query(
            Product.id,
            Product.name,
            func.coalesce(func.sum(Inventory.quantity_change), 0).label("stock")
        )
        .outerjoin(Inventory, Inventory.product_id == Product.id)
        .group_by(Product.id, Product.name)
        .all()
    )

    if not inventory_data:
        raise HTTPException(status_code=404, detail="No inventory data found")

    result = [
        {"id": item.id, "name": item.name, "stock": item.stock}
        for item in inventory_data
    ]
    return result

@app.get("/inventory/low-stock")
async def get_low_stock_inventory(threshold: int = 10, db: Session = Depends(get_db)):
    # Calculate stock per product and filter by threshold
    low_stock_products = (
        db.query(
            Product.id,
            Product.name,
            func.coalesce(func.sum(Inventory.quantity_change), 0).label("stock")
        )
        .outerjoin(Inventory, Inventory.product_id == Product.id)
        .group_by(Product.id, Product.name)
        .having(func.coalesce(func.sum(Inventory.quantity_change), 0) < threshold)
        .all()
    )

    if not low_stock_products:
        return {"message": "No products are low in stock"}

    results = [
        {"id": p.id, "name": p.name, "stock": p.stock}
        for p in low_stock_products
    ]
    return results

@app.put("/inventory/{product_id}")
async def update_inventory(product_id: int, quantity_change: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Add a new inventory record to track the change
    new_inventory_entry = Inventory(product_id=product_id, quantity_change=quantity_change, quantity=None)
    db.add(new_inventory_entry)
    db.commit()
    db.refresh(new_inventory_entry)

    return {"message": "Inventory updated successfully", "inventory_id": new_inventory_entry.id}

# Product Endpoints
@app.post("/products")
async def add_product(name: str, price: float, category: str, db: Session = Depends(get_db)):
    new_product = Product(name=name, price=price, category=category)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"message": "Product added successfully", "product_id": new_product.id}

@app.get("/sales_data")
async def get_all_sales(db: Session = Depends(get_db)):
    sales = db.query(Sale).all()

    if not sales:
        raise HTTPException(status_code=404, detail="No sales data found")

    result = [
        {
            "id": s.id,
            "product_id": s.product_id,
            "total_amount": s.total_amount,
            "sale_date": s.sale_date.isoformat()
        }
        for s in sales
    ]

    return result

@app.get("/products")
async def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()

    if not products:
        raise HTTPException(status_code=404, detail="No products found")

    result = [
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "category": p.category
        }
        for p in products
    ]

    return result

# New endpoint: get sales aggregated by product category
@app.get("/sales/category/{category_name}")
async def get_sales_by_category(category_name: str, db: Session = Depends(get_db)):
    sales_data = (
        db.query(
            Product.category,
            func.sum(Sale.total_amount).label("total_sales")
        )
        .join(Sale, Sale.product_id == Product.id)
        .filter(Product.category == category_name)
        .group_by(Product.category)
        .first()
    )
    if not sales_data:
        raise HTTPException(status_code=404, detail="No sales found for this category")

    return {
        "category": sales_data.category,
        "total_sales": sales_data.total_sales
    }


@app.get("/sales/filter")
async def get_sales_by_product_and_category(
    product_name: str = None, 
    category: str = None, 
    db: Session = Depends(get_db)
):
    query = db.query(
        Product.id.label("product_id"),
        Product.name,
        Product.category,
        func.sum(Sale.total_amount).label("total_sales")
    ).join(Sale, Sale.product_id == Product.id)

    if product_name:
        query = query.filter(Product.name.ilike(f"%{product_name}%"))
    if category:
        query = query.filter(Product.category.ilike(f"%{category}%"))

    query = query.group_by(Product.id, Product.name, Product.category)

    results = query.all()

    if not results:
        raise HTTPException(status_code=404, detail="No sales data found for the given filters")

    return [
        {
            "product_id": r.product_id,
            "product_name": r.name,
            "category": r.category,
            "total_sales": r.total_sales,
        }
        for r in results
    ]

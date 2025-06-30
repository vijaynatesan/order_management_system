from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
from fastapi_mcp import FastApiMCP
from dotenv import load_dotenv

models.Base.metadata.create_all(bind=engine)

load_dotenv()
app = FastAPI()



# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# List all orders endpoint
@app.get("/orders/", response_model=list[schemas.ItemOrder], operation_id="read_orders", summary="Retrieve a list of all orders.")
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders

# Delete customer endpoint
@app.delete("/customers/{customer_id}", response_model=schemas.Customer, operation_id="delete_customer", summary="Delete a customer by their unique ID.")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud.delete_customer(db, customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

# Delete order endpoint
@app.delete("/orders/{order_id}", response_model=schemas.ItemOrder, operation_id="delete_order", summary="Delete an order by its unique ID.")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.delete_order(db, order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

# Delete reorder log endpoint
@app.delete("/reorder_logs/{log_id}", response_model=schemas.ItemReorderLog, operation_id="delete_reorder_log", summary="Delete a reorder log by its unique ID.")
def delete_reorder_log(log_id: int, db: Session = Depends(get_db)):
    db_log = crud.delete_reorder_log(db, log_id)
    if db_log is None:
        raise HTTPException(status_code=404, detail="Reorder log not found")
    return db_log

@app.post("/customers/", response_model=schemas.Customer, operation_id="create_customer", summary="Create a new customer.")
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db=db, customer=customer)

@app.post("/items/", response_model=schemas.Item, operation_id="create_item", summary="Create a new item.")
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item)

@app.put("/customers/{customer_id}", response_model=schemas.Customer, operation_id="update_customer", summary="Update an existing customer by ID.")
def update_customer(customer_id: int, customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    db_customer = crud.update_customer(db, customer_id, customer)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@app.get("/customers/", response_model=list[schemas.Customer], operation_id="read_customers", summary="Retrieve a list of all customers. Do not use this when searching by customer name. For searching by name use read_customer_by_name.")
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = crud.get_customers(db, skip=skip, limit=limit)
    return customers

@app.get("/customers/{customer_id}", response_model=schemas.Customer, operation_id="read_customer", summary="Retrieve a customer by their unique ID.")
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@app.get("/customers/by_name/{name}", response_model=list[schemas.Customer], operation_id="read_customer_by_name", summary="Retrieve customers by partial name match.")
def read_customer_by_name(name: str, db: Session = Depends(get_db)):
    db_customers = crud.get_customer_by_name(db, name=name)
    if not db_customers:
        raise HTTPException(status_code=404, detail="No customers found")
    return db_customers



@app.put("/items/{item_id}", response_model=schemas.Item, operation_id="update_item", summary="Update an existing item by ID.")
def update_item(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = crud.update_item(db, item_id, item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.get("/items/", response_model=list[schemas.Item], operation_id="read_items", summary="Retrieve a list of all items. Do not use this when searching by item name. For searching by name use read_item_by_name.")
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@app.get("/items/{item_id}", response_model=schemas.Item, operation_id="read_item", summary="Retrieve an item by its unique ID.")
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.get("/items/by_name/{name}", response_model=list[schemas.Item], operation_id="read_item_by_name", summary="Retrieve items by partial name match.")
def read_item_by_name(name: str, db: Session = Depends(get_db)):
    db_items = crud.get_item_by_name(db, name=name)
    if not db_items:
        raise HTTPException(status_code=404, detail="No items found")
    return db_items

# Delete item endpoint
@app.delete("/items/{item_id}", response_model=schemas.Item, operation_id="delete_item", summary="Delete an item by its unique ID.")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.post("/orders/", response_model=schemas.ItemOrder, operation_id="create_order", summary="Create a new order for an item if sufficient stock is available.")
def create_order(order: schemas.ItemOrderCreate, db: Session = Depends(get_db)):
    db_order = crud.create_order(db, order)
    if db_order is None:
        raise HTTPException(status_code=400, detail="Order quantity exceeds available stock")
    return db_order

@app.get("/reorder_logs/", response_model=list[schemas.ItemReorderLog], operation_id="read_reorder_logs", summary="Retrieve a list of reorder logs for items.")
def read_reorder_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reorder_logs = crud.get_reorder_logs(db, skip=skip, limit=limit)
    return reorder_logs

mcp = FastApiMCP(app, name="VNOMS", 
                 include_operations=['create_order','read_customers','read_items','create_customer','read_item_by_name','read_orders'],
                 description="This is VIJAY NATESAN's Order Management System. When someone searches a prodct by name, always use read_item_by_name")
mcp.mount()
mcp.setup_server()
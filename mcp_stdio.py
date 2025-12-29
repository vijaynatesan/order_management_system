import sys
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP

import crud, schemas
from database import SessionLocal, engine
import models

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

mcp = FastMCP("VNOMS")

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

def orm_to_dict(obj):
    """Convert SQLAlchemy ORM object to dict, excluding internal attributes."""
    return {k: v for k, v in obj.__dict__.items() if not k.startswith('_')}

@mcp.tool()
def read_items(skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    """Retrieve a list of all items."""
    db = SessionLocal()
    try:
        items = crud.get_items(db, skip=skip, limit=limit)
        # Convert ORM objects to plain dicts
        return [orm_to_dict(i) for i in items]
    finally:
        db.close()

@mcp.tool()
def read_item_by_name(name: str) -> List[Dict[str, Any]]:
    """Search items by partial name match (preferred for item search)."""
    db = SessionLocal()
    try:
        items = crud.get_item_by_name(db, name=name)
        return [orm_to_dict(i) for i in items]
    finally:
        db.close()

@mcp.tool()
def read_customers(skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    """Retrieve a list of all customers."""
    db = SessionLocal()
    try:
        customers = crud.get_customers(db, skip=skip, limit=limit)
        return [orm_to_dict(c) for c in customers]
    finally:
        db.close()

@mcp.tool()
def read_orders(skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    """Retrieve a list of all orders."""
    db = SessionLocal()
    try:
        orders = crud.get_orders(db, skip=skip, limit=limit)
        return [orm_to_dict(o) for o in orders]
    finally:
        db.close()

@mcp.tool()
def create_customer(name: str, address: str, zip_code: str, segment: str) -> Dict[str, Any]:
    """Create a new customer."""
    db = SessionLocal()
    try:
        payload = schemas.CustomerCreate(name=name, address=address, zip_code=zip_code, segment=segment)
        customer = crud.create_customer(db=db, customer=payload)
        return orm_to_dict(customer)
    finally:
        db.close()

@mcp.tool()
def create_order(item_id: int, customer_id: int, order_quantity: int, discount: float) -> Dict[str, Any]:
    """Create a new order if sufficient stock is available."""
    db = SessionLocal()
    try:
        payload = schemas.ItemOrderCreate(item_id=item_id, customer_id=customer_id, order_quantity=order_quantity, discount=discount, original_price=0.0, discounted_price=0.0)  # prices will be calculated
        order = crud.create_order(db, payload)
        if order is None:
            return {"error": "Order quantity exceeds available stock"}
        return orm_to_dict(order)
    finally:
        db.close()

@mcp.tool()
def delete_customer(customer_id: int) -> Optional[Dict[str, Any]]:
    """Delete a customer by ID."""
    db = SessionLocal()
    try:
        customer = crud.delete_customer(db, customer_id=customer_id)
        return orm_to_dict(customer) if customer else None
    finally:
        db.close()

@mcp.tool()
def delete_order(order_id: int) -> Optional[Dict[str, Any]]:
    """Delete an order by ID."""
    db = SessionLocal()
    try:
        order = crud.delete_order(db, order_id=order_id)
        return orm_to_dict(order) if order else None
    finally:
        db.close()

@mcp.tool()
def delete_reorder_log(log_id: int) -> Optional[Dict[str, Any]]:
    """Delete a reorder log by ID."""
    db = SessionLocal()
    try:
        log = crud.delete_reorder_log(db, log_id=log_id)
        return orm_to_dict(log) if log else None
    finally:
        db.close()

@mcp.tool()
def read_customer(customer_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve a customer by ID."""
    db = SessionLocal()
    try:
        customer = crud.get_customer(db, customer_id=customer_id)
        return orm_to_dict(customer) if customer else None
    finally:
        db.close()

@mcp.tool()
def read_customer_by_name(name: str) -> List[Dict[str, Any]]:
    """Search customers by partial name match."""
    db = SessionLocal()
    try:
        customers = crud.get_customer_by_name(db, name=name)
        return [orm_to_dict(c) for c in customers]
    finally:
        db.close()

@mcp.tool()
def update_customer(customer_id: int, name: str, address: str, zip_code: str, segment: str) -> Optional[Dict[str, Any]]:
    """Update a customer by ID."""
    db = SessionLocal()
    try:
        payload = schemas.CustomerCreate(name=name, address=address, zip_code=zip_code, segment=segment)
        customer = crud.update_customer(db, customer_id=customer_id, customer=payload)
        return orm_to_dict(customer) if customer else None
    finally:
        db.close()

@mcp.tool()
def create_item(name: str, description: str, manufacturer_name: str, manufacturer_email: str, price: float, in_stock: int, reorder_quantity: int) -> Dict[str, Any]:
    """Create a new item."""
    db = SessionLocal()
    try:
        payload = schemas.ItemCreate(name=name, description=description, manufacturer_name=manufacturer_name, manufacturer_email=manufacturer_email, price=price, in_stock=in_stock, reorder_quantity=reorder_quantity)
        item = crud.create_item(db=db, item=payload)
        return orm_to_dict(item)
    finally:
        db.close()

@mcp.tool()
def update_item(item_id: int, name: str, description: str, manufacturer_name: str, manufacturer_email: str, price: float, in_stock: int, reorder_quantity: int) -> Optional[Dict[str, Any]]:
    """Update an item by ID."""
    db = SessionLocal()
    try:
        payload = schemas.ItemCreate(name=name, description=description, manufacturer_name=manufacturer_name, manufacturer_email=manufacturer_email, price=price, in_stock=in_stock, reorder_quantity=reorder_quantity)
        item = crud.update_item(db, item_id=item_id, item=payload)
        return orm_to_dict(item) if item else None
    finally:
        db.close()

@mcp.tool()
def delete_item(item_id: int) -> Optional[Dict[str, Any]]:
    """Delete an item by ID."""
    db = SessionLocal()
    try:
        item = crud.delete_item(db, item_id=item_id)
        return orm_to_dict(item) if item else None
    finally:
        db.close()

@mcp.tool()
def read_reorder_logs(skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    """Retrieve a list of reorder logs."""
    db = SessionLocal()
    try:
        logs = crud.get_reorder_logs(db, skip=skip, limit=limit)
        return [orm_to_dict(l) for l in logs]
    finally:
        db.close()


if __name__ == "__main__":
    # IMPORTANT: log to stderr only (stdout is MCP protocol)
    print("Starting VNOMS MCP (stdio)...", file=sys.stderr)
    mcp.run()
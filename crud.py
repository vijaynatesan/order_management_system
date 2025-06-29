
from sqlalchemy.orm import Session
import models, schemas

def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def get_customer_by_name(db: Session, name: str):
    return db.query(models.Customer).filter(models.Customer.name == name).first()

def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Customer).offset(skip).limit(limit).all()

def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(db: Session, customer_id: int, customer: schemas.CustomerCreate):
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if db_customer:
        for key, value in customer.model_dump().items():
            setattr(db_customer, key, value)
        db.commit()
        db.refresh(db_customer)
    return db_customer

def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def get_item_by_name(db: Session, name: str):
    return db.query(models.Item).filter(models.Item.name == name).first()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item: schemas.ItemCreate):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        for key, value in item.model_dump().items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item

# Delete item
def delete_item(db: Session, item_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return db_item
    return None

def create_order(db: Session, order: schemas.ItemOrderCreate):
    db_item = db.query(models.Item).filter(models.Item.id == order.item_id).first()
    if db_item and db_item.in_stock >= order.order_quantity:
        db_order = models.ItemOrder(**order.model_dump())
        db_item.in_stock -= order.order_quantity
        if db_item.in_stock < db_item.reorder_quantity:
            db_reorder_log = models.ItemReorderLog(item_id=order.item_id)
            db.add(db_reorder_log)
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order
    return None

def get_reorder_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ItemReorderLog).offset(skip).limit(limit).all()

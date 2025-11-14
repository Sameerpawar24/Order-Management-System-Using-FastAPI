import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from sqlalchemy.orm import Session
from models.products import Product
from models.audit import AuditLog
from fastapi import HTTPException,status

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_products(db: Session, skip=0, limit=100):
    return db.query(Product).offset(skip).limit(limit).all()

def create_product(db: Session, **kwargs):
    p = Product(**kwargs)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

def change_stock(db: Session, product: Product, delta: int, performed_by: int = None, note: str = None):
    before = {"stock": product.stock}
    product.stock = product.stock + delta
    if product.stock < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={'status_code':status.HTTP_400_BAD_REQUEST,'messege':"You Dont Have enough stock To Change"})
    db.add(product)
    db.commit()
    db.refresh(product)

    audit = AuditLog(entity="product", entity_id=product.id, action="stock_change",
                     performed_by=performed_by, before=before, after={"stock": product.stock})
    db.add(audit)
    db.commit()
    return product


def delete_product(db:Session,product_id:int):
    product= db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None    
    db.delete(product)      
    db.commit()    

    audit = AuditLog(entity="product", entity_id=product_id, action="Product delete",
                     performed_by='Admin', before=0, after='deleted')
    db.add(audit)
    db.commit()         
    return product 
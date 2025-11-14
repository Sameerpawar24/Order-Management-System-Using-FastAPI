from sqlalchemy.orm import Session
from models.orders import Order, OrderItem, OrderStatusHistory, OrderStatus
from models.products import Product
from models.audit import AuditLog
from decimal import Decimal
from fastapi import HTTPException,status
from fastapi.responses import JSONResponse


def place_order(db: Session, user_id: int, shipping_address: dict, items: list):

    # items → list of { "product_id": int, "quantity": int }

    if not items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Order must contain at least one item"}
        )

    total = Decimal(0)

    # Create base order entry first
    order = Order(
        user_id=user_id,
        total_amount=total,
        shipping_address=shipping_address
    )
    db.add(order)
    db.flush()  # assigns order.id

    for it in items:
        product_id = it["product_id"]
        qty = it["quantity"]

        # Lock row for stock update
        product = (
            db.query(Product).filter(Product.id == product_id).with_for_update().first()
        )

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message": f"Product {product_id} not found"}
            )

        # Stock check
        if product.stock < qty:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": f"Insufficient stock for product {product_id}"}
            )

        # Deduct stock
        before_stock = product.stock
        product.stock -= qty
        after_stock = product.stock

        # Calculate item amount
        unit_price = product.price
        line_total = unit_price * qty
        total += line_total

        # Add order item
        order_item = OrderItem(
            order_id=order.id,
            product_id=product_id,
            quantity=qty,
            unit_price=unit_price
        )
        db.add(order_item)

        # Audit log
        audit = AuditLog(
            entity="product",
            entity_id=product_id,
            action="stock_decrement",
            before={"stock": before_stock},
            after={"stock": after_stock}
        )
        db.add(audit)

    # Update final order total
    order.total_amount = total
    db.add(order)

    # Initial order status
    status_entry = OrderStatusHistory(
        order_id=order.id,
        previous_status="",
        new_status=OrderStatus.created.value
    )
    db.add(status_entry)

    db.commit()
    db.refresh(order)

    return order


def change_order_status(db: Session, order: Order, new_status: OrderStatus, changed_by: int = None, note: str = None):
    # validate transitions
    current = order.status
    allowed = {
        OrderStatus.created: [OrderStatus.processed],
        OrderStatus.processed: [OrderStatus.shipped],
        OrderStatus.shipped: [OrderStatus.delivered],
        OrderStatus.delivered: []
    }
    if new_status == current:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Status Is In Already Given Requested Status"}
        )
    if new_status not in allowed[current]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": f"Invalid status transition from {current} to {new_status}"}
        )

        #raise ValueError(f"Invalid status transition from {current} to {new_status}")

    prev = current.value
    order.status = new_status
    db.add(order)
    hist = OrderStatusHistory(order_id=order.id, previous_status=prev, new_status=new_status.value, changed_by=changed_by, note=note)
    db.add(hist)
    audit = AuditLog(entity="order", entity_id=order.id, action="status_change", performed_by=changed_by, before={"status": prev}, after={"status": new_status.value})
    db.add(audit)
    db.commit()
    db.refresh(order)
    return order


def get_status_order(db:Session,order_id:int):
    return db.query(OrderStatusHistory).filter(OrderStatusHistory.order_id == order_id).order_by(OrderStatusHistory.new_status.desc()).first()
    
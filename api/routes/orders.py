from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from api.deps import get_db, get_current_user, require_roles
from schema.orders_schema import OrderCreate, OrderRead, OrderStatusUpdate
from crud.orders_crud import place_order, change_order_status,get_status_order
from models.orders import OrderStatus, Order
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api/orders", tags=["orders"])

@router.post("/", response_model=OrderRead)
def create_order(payload: OrderCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        order = place_order(db, user_id=current_user.id, shipping_address=payload.shipping_address.dict(), items=[it.dict() for it in payload.items])
        return JSONResponse(content={'status_code':status.HTTP_200_OK,'messege':"Your Order Created Successfully",'details':{'order_id':order.id,'Current_order_status':order.status}})
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.get("/{order_id}", response_model=OrderRead)
def get_order(order_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'status_code': status.HTTP_404_NOT_FOUND, 'message': "Order not found"}
        )
    # restrict customers to see their own orders only.
    if current_user.role.value == "customer" and order.user_id != current_user.id:
         return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={'status_code': status.HTTP_401_UNAUTHORIZED, 'message': "You are not authorized to see the order details"})
    return order
    

@router.post("/{order_id}/status", dependencies=[Depends(require_roles("admin", "customer_support"))])
def update_status(order_id: int, payload: OrderStatusUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id).first()
  
    if not order:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'status_code': status.HTTP_404_NOT_FOUND, 'message': "Order not found"}
        )
    try:
        new_status = OrderStatus(payload.new_status)
    except ValueError:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'status_code': status.HTTP_400_BAD_REQUEST, 'message': "Invalid Status Value"}
        )
    try:
        
        updated = change_order_status(db, order, new_status, changed_by=current_user.id, note=current_user.full_name)
        return {'message': "Order Status Has Been Updated",'details':{'current_status':updated.status}}
        # return updated
    except ValueError as e:
        raise HTTPException(409, str(e))


@router.get("/{order_id}/get_status")
def get_order_s(order_id:int,db:Session=Depends(get_db)):
    return get_status_order(order_id=order_id,db=db)


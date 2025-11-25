import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from crud.product_crud import get_products, create_product, get_product, change_stock, delete_product
from schema.products_schema import ProductCreate, ProductRead, StockUpdate
from api.deps import get_db, require_permission
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api/products", tags=["Products"])

@router.get("/", response_model=list[ProductRead])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_products(db, skip=skip, limit=limit)

@router.post("/", dependencies=[Depends(require_permission("products.create"))])
def create_product_route(payload: ProductCreate, db: Session = Depends(get_db)):
    create_product(db, **payload.dict())
    return JSONResponse(content={'status_code': status.HTTP_200_OK, 'message': 'Product created successfully'})

@router.patch("/{product_id}/stock", dependencies=[Depends(require_permission("products.update_stock"))])
def update_stock(product_id: int, payload: StockUpdate, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(404, "Product not found")
    change_stock(db, product, payload.delta, note=payload.note)
    return JSONResponse(content={'status_code':status.HTTP_200_OK,"messege":"Stock is Update Successfully",'details':{'updated stock':product.stock}})

@router.delete("/{product_id}", dependencies=[Depends(require_permission("products.delete"))])
def delete_product_route(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(404, "Product not found")
    delete_product(db, product_id)
    return {"status_code": 200, "message": "Product delete successfully"}



# from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.responses import JSONResponse
# from sqlalchemy.orm import Session

# from api.deps import get_db, get_current_user, require_roles
# from schema.products_schema import ProductCreate, ProductRead, StockUpdate
# from crud.product_crud import (
#     get_products,
#     create_product,
#     get_product,
#     change_stock,
#     delete_product
# )

# router = APIRouter(prefix="/api/products", tags=["products"])

# # -------------------------------------------------------------
# # List all products
# # -------------------------------------------------------------
# @router.get("/", response_model=list[ProductRead])
# def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     return get_products(db, skip=skip, limit=limit)


# # -------------------------------------------------------------
# # Create Product (Admin only)
# # -------------------------------------------------------------
# @router.post("/", dependencies=[Depends(require_roles("admin"))])
# def create_product_route(p: ProductCreate, db: Session = Depends(get_db)):
#     product = create_product(db, **p.dict())

#     return JSONResponse(
#         status_code=status.HTTP_201_CREATED,
#         content={
#             "status": True,
#             "message": "Product created successfully",
#             "product": product.id
#         }
#     )


# # -------------------------------------------------------------
# # Update Stock (Admin only)
# # -------------------------------------------------------------
# @router.patch(
#     "/{product_id}/stock",
#     dependencies=[Depends(require_roles("admin"))]
# )
# def update_stock(
#     product_id: int,
#     payload: StockUpdate,
#     db: Session = Depends(get_db),
#     current_user=Depends(get_current_user)
# ):
#     product = get_product(db, product_id)
#     if not product:
#         raise HTTPException(404, "Product not found")

#     try:
#         updated_product = change_stock(
#             db,
#             product=product,
#             delta=payload.delta,
#             performed_by=current_user.id,
#             note=payload.note
#         )
#         return {
#             "message": "Stock updated successfully",
#             "current_stock": updated_product.stock
#         }

#     except ValueError as e:
#         raise HTTPException(400, str(e))


# # -------------------------------------------------------------
# # Delete Product (Admin only)
# # -------------------------------------------------------------
# @router.delete(
#     "/{product_id}",
#     dependencies=[Depends(require_roles("admin"))]
# )
# def delete_product_route(product_id: int, db: Session = Depends(get_db)):
#     product = get_product(db, product_id)

#     if not product:
#         raise HTTPException(404, "Product not found")

#     delete_product(db, product_id)

#     return JSONResponse(
#         status_code=status.HTTP_200_OK,
#         content={
#             "status": True,
#             "message": "Product deleted successfully"
#         }
#     )




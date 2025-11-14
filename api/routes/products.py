from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.deps import get_db, require_roles
from schema.products_schema import ProductCreate, ProductRead, StockUpdate
from crud.product_crud import get_products, create_product, get_product, change_stock,delete_product
from fastapi.responses import JSONResponse
from fastapi import status
router = APIRouter(prefix="/api/products", tags=["products"])

@router.get("/", response_model=list[ProductRead])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_products(db, skip=skip, limit=limit)

@router.post("/", response_model=ProductRead, dependencies=[Depends(require_roles("admin"))])
def create(p: ProductCreate, db: Session = Depends(get_db)):
    create_product(db, **p.dict())
    return JSONResponse(content={'status_code':status.HTTP_200_OK,'messege':'Product Created Successfully'})
#create_product(db, **p.dict())

@router.patch("/{product_id}/stock", dependencies=[Depends(require_roles("admin"))])
def update_stock(product_id: int, payload: StockUpdate, db: Session = Depends(get_db), current_user=Depends(require_roles("admin"))):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(404, "Product not found")
    try:
        return change_stock(db, product, payload.delta, performed_by=current_user.id, note=payload.note)
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.delete("/{product_id}", dependencies=[Depends(require_roles("admin"))])
def delete_product_route(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    delete_product(db, product_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status_code": status.HTTP_200_OK,
            "message": "Product deleted successfully"
        }
    )
    #return delete_product(db,product_id)


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.stock import Stock
from app.schemas.stock import StockCreate, StockResponse, StockUpdate


router = APIRouter(prefix="/stock", tags=["stock"])


@router.get("/", response_model=list[StockResponse])
def get_stocks(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(Stock).offset(skip).limit(limit).all()


@router.get("/{stock_id}", response_model=StockResponse)
def get_stock(stock_id: int, db: Session = Depends(get_db)):
    stock = db.query(Stock).filter(Stock.id == stock_id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock


@router.post("/", response_model=StockResponse, status_code=status.HTTP_201_CREATED)
def create_stock(stock_data: StockCreate, db: Session = Depends(get_db)):
    existing = db.query(Stock).filter(Stock.product_id == stock_data.product_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Stock for this product already exists")
    
    stock = Stock(**stock_data.dict())
    db.add(stock)
    db.commit()
    db.refresh(stock)
    return stock


@router.put("/{stock_id}", response_model=StockResponse)
def update_stock(stock_id: int, stock_data: StockUpdate, db: Session = Depends(get_db)):
    stock = db.query(Stock).filter(Stock.id == stock_id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    for key, value in stock_data.dict(exclude_unset=True).items():
        setattr(stock, key, value)
    
    db.commit()
    db.refresh(stock)
    return stock


@router.delete("/{stock_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_stock(stock_id: int, db: Session = Depends(get_db)):
    stock = db.query(Stock).filter(Stock.id == stock_id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    db.delete(stock)
    db.commit()
    return

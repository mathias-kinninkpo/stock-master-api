# routes/stock_movement.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from functions.stock_movement import create_stock_movement, get_stock_movements, get_stock_movement
from schemas.stock_movement import StockMovementCreate, StockMovement as  StockMovementResponse
from .auth import get_current_user, get_db



stock_router = APIRouter(prefix="/stock_movements", tags=["Stock Movements"], dependencies=[Depends(get_current_user)])

@stock_router.post("/", response_model=StockMovementResponse)
def create_stock(stock_movement: StockMovementCreate, db: Session = Depends(get_db)):
    return create_stock_movement(db, stock_movement)

@stock_router.get("/", response_model=list[StockMovementResponse])
def read_stock_movements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_stock_movements(db, skip=skip, limit=limit)

@stock_router.get("/{movement_id}", response_model=StockMovementResponse)
def read_stock_movement(movement_id: int, db: Session = Depends(get_db)):
    _stock_movement = get_stock_movement(db, movement_id)
    if _stock_movement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='stock not found'
        )
    return _stock_movement


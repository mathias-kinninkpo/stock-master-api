# functions/stock_movement.py
from sqlalchemy.orm import Session
from schemas.stock_movement import StockMovementCreate, StockMovement as StockMovementResponse
from models.stock_movement import StockMovement
from functions.product import update_product_quantity

def create_stock_movement(db: Session, stock_movement: StockMovementCreate):
    with db.begin():
        db_stock_movement = StockMovement(**stock_movement.dict())
        db.add(db_stock_movement)
        db.commit()
        db.refresh(db_stock_movement)

        # Mise à jour de la quantité en stock dans la table des produits
        update_product_quantity(db, stock_movement.product_id, stock_movement.quantity, stock_movement.movement_type)

    return StockMovementResponse.from_orm(db_stock_movement)

def get_stock_movements(db: Session, skip: int = 0, limit: int = 10):
    stock_movements = db.query(StockMovement).offset(skip).limit(limit).all()
    if not stock_movements:
        return None
    return [StockMovementResponse.from_orm(movement) for movement in stock_movements]

def get_stock_movement(db: Session, movement_id: int):
    db_movement = db.query(StockMovement).filter(StockMovement.movement_id == movement_id).first()
    if db_movement is None:
        return None
    return StockMovementResponse.from_orm(db_movement)



from pydantic import BaseModel
from datetime import datetime
from typing import List

class StockMovementBase(BaseModel):
    product_id: int
    movement_type: str
    quantity: int
    movement_date: datetime
    notes: str

class StockMovementCreate(StockMovementBase):
    pass

class StockMovement(StockMovementBase):
    movement_id: int

    class Config:
        orm_mode = True
        from_attributes=True


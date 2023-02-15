from datetime import datetime
from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pydantic.types import PositiveInt, Any
from .calculator import Calculator

app = FastAPI(title="Delivery Fee Calculator API")


class DeliveryFeeRequest(BaseModel):
    cart_value: PositiveInt
    delivery_distance: PositiveInt
    number_of_items: PositiveInt
    time: datetime


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: DeliveryFeeRequest, exc: Any) -> Any:
    message = "You inserted invalid type of data on the fields."
    return JSONResponse(
        content={"msg": message}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


@app.get("/")
async def home() -> dict[str, str]:
    return {"Welcome to": "FastAPI Delivery Fee Calculator"}


@app.post("/calculator/")
async def calculator(request: DeliveryFeeRequest) -> dict[str, PositiveInt]:
    calc = Calculator(
        request.cart_value,
        request.delivery_distance,
        request.number_of_items,
        request.time,
    )
    delivery_fee = calc.get_delivery_fee()

    return {"delivery_fee": delivery_fee}

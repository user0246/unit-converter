from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="public")

COEFFICIENTS_TO_METER = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1,
    "km": 1000,
    "in": 0.0254,
    "ft": 0.3048,
    "yd": 0.9144,
    "mi": 1609.344
}

COEFFICIENTS_TO_GRAM = {
    "mg": 0.001,
    "g": 1,
    "kg": 1000,
    "oz": 28.349523,
    "lb": 453.59237
}

@app.get("/")
def index(request : Request, app_type: str = "length"):
    if app_type == "length":
        units = COEFFICIENTS_TO_METER
    elif app_type == "weight":
        units = COEFFICIENTS_TO_GRAM
    else:
        units = ["C", "K", "F"]

    return templates.TemplateResponse(name="index.html", request=request,context={
        "app": app_type,
        "units": units
    })

@app.post("/length")
def length(value: float = Form(), unit_from: str = Form(), unit_to: str = Form()):
    result = value * COEFFICIENTS_TO_METER[unit_from] / COEFFICIENTS_TO_METER[unit_to]
    return result

@app.post("/weight")
def weight(value: float = Form(), unit_from: str = Form(), unit_to: str = Form()):
    result = value * COEFFICIENTS_TO_GRAM[unit_from] / COEFFICIENTS_TO_GRAM[unit_to]
    return result

@app.post("/temperature")
def temperature(value: float = Form(), unit_from: str = Form(), unit_to: str = Form()):
    if unit_from == "C":
        result = value
    elif unit_from == "K":
        result = value - 273.15
    elif unit_from == "F":
        result = (value - 32) * 5 / 9

    if unit_to == "C":
        return result
    elif unit_to == "K":
        return result + 273.15
    elif unit_to == "F":
        return (result * 9 / 5) + 32
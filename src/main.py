from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, FileResponse
from src.routes import users, orders, items

HTML_PATH = "UI/Ui.html"

app = FastAPI()
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(items.router)


@app.get("/favicon.ico")
async def favicon():
    return FileResponse("src/static/favicon.ico")


@app.get("/")
def root():
    return FileResponse(HTML_PATH)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    error_details = []
    for error in errors:
        error_type = error["type"]
        error_location = error["loc"][1]
        error_message = error["msg"]

        if error_message == "JSON decode error":
            ctx = error["ctx"]["error"]
            error_details.append(f"Type: {error_type}, Position: {error_location} - {error_message} - {ctx}")
        else:
            error_details.append(f"Type: {error_type}, Field: {error_location} - {error_message}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": "Validation failed",
            "details": error_details
        }
    )

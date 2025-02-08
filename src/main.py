
from fastapi import FastAPI

from src.routes import users,customers,orders,items
from fastapi.responses import FileResponse


HTML_PATH = "UI/Ui.html"

app = FastAPI()
app.include_router(users.router)
app.include_router(customers.router)
app.include_router(orders.router)
app.include_router(items.router)


@app.get("/")
def root():
    return FileResponse(HTML_PATH)


from fastapi import FastAPI

from src.routes import users,orders,items
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


HTML_PATH = "UI/Ui.html"

app = FastAPI()
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(items.router)


# Обработчик для favicon.ico
@app.get("/favicon.ico")
async def favicon():
    return FileResponse("src/static/favicon.ico")

@app.get("/")
def root():
    return FileResponse(HTML_PATH)



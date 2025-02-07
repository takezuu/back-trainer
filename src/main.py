
from fastapi import FastAPI


from src import routes
from fastapi.responses import FileResponse


HTML_PATH = "UI/Ui.html"

app = FastAPI()
app.include_router(routes.router)


@app.get("/")
def root():
    return FileResponse(HTML_PATH)

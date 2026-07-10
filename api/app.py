from fastapi import FastAPI

from api.db_settings import apply_sql_views

from api.routes import main_router

app = FastAPI(
    tittle="Tá Na Mesa form responses API",
    description="", 
    version="1.0.0"
)

app.include_router(main_router.router)

@app.get("/healthy")
def health_check():
    return {"status": "healthy"}

@app.on_event("startup")
def on_startup():
    apply_sql_views()
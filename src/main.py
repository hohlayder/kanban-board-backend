import uvicorn
from fastapi import FastAPI

from src.settings import settings
from src.routers import router

app = FastAPI(debug=settings.SERVER_TEST)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=settings.SERVER_ADDR,
        port=settings.SERVER_PORT,
        log_level="debug" if settings.SERVER_TEST else "info",
        reload=True
    )

import uvicorn
from fastapi import FastAPI

from app.api import user_router
from app.settings import conf

app = FastAPI(version=conf.version)
app.include_router(user_router, tags=["Routers"])

if __name__ == '__main__':
    uvicorn.run(app, host=conf.host, port=conf.port)

from code.routers import invocations
from fastapi import FastAPI
app = FastAPI()
app.include_router(invocations.router)
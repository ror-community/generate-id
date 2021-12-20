from fastapi import FastAPI
from typing import Optional
from starlette.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import httpx
import os

app = FastAPI()

HEADERS = {'Token': os.environ["TOKEN"], 'Route-User': os.environ["ROUTE_USER"]}
URL = os.environ["ROR_API_URL"]

origins = [
    os.environ['ALLOWED_ORIGINS']
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/generateid")
async def get_ror_id(mode: Optional[str] = None):
    # if being sent in any mode but production
    # mock an id
    if mode:
        data = {'id':'https://ror.org/012DEV089'}
        response = data
    else:
        async with httpx.AsyncClient() as client:
            response = await client.get(URL, headers=HEADERS)
            response = response.json()
    return response

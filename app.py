from fastapi import FastAPI, Request, Response, status
from typing import Optional
from starlette.middleware.cors import CORSMiddleware
import httpx
import os
import logging as logger
import sys

app = FastAPI()

logger.basicConfig(encoding='utf-8',level=logger.DEBUG,stream = sys.stdout)

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
def info(request: Request):
    logger.info(f"{request.method} {request.url}")

async def handle_http_request(request: Request, response: Response, url, error_status = "500", **kwargs):
    logger.info(info(request))
    async with httpx.AsyncClient() as client:
            try:
                if ('username' in kwargs) and ('geonameId' in kwargs):
                    response = await client.get(url, params = kwargs)
                else:
                    response = await client.get(url, headers = {'Token': os.environ["TOKEN"], 'Route-User': os.environ["ROUTE_USER"]})
                response.raise_for_status()
            except httpx.RequestError as exc:
                response.status_code = error_status
                logger.error(f"An error occurred while requesting {exc.request.url!r}.")
            except httpx.HTTPStatusError as exc:
                response.status_code = exc.response.status_code
                logger.error(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
    return response

@app.get("/heartbeat")
def response(request:Request):
    logger.info(info(request))
    return {'status': 'OK'}

@app.get("/address")
async def get_address(locationid: int, request: Request, response: Response):
    params = { "username": "roradmin", "geonameId": locationid }
    geonames_url = "http://api.geonames.org/getJSON"
    response = await handle_http_request(request, response, url=geonames_url, error_status="400", **params)
    try:
        if response and response.json():
            return response.json()
    except Exception as e:
        return e

@app.get("/generateid")
async def get_ror_id(request: Request, response: Response, mode: Optional[str] = None):
    # if being sent in any mode but production
    # mock an id
    logger.info(info(request))
    if mode:
        data = {'id':'https://ror.org/012dev089'}
        response = data
    else:
        request_url = URL + request.url.path
        response = await handle_http_request(request, response, url=request_url, error_status=status.HTTP_503_SERVICE_UNAVAILABLE, **HEADERS)
        try:
            if response and response.json():
                response = response.json()
        except Exception as e:
            return e
    return response

@app.get("/indexdata")
async def index_new_records(request: Request, response: Response):
    logger.info(info(request))
    request_url = URL + request.url.path
    response = await handle_http_request(request, response, url=request_url, error_status=status.HTTP_503_SERVICE_UNAVAILABLE, **HEADERS)
    try:
        if response and response.json():
            response = response.json()
    except Exception as e:
        return e
    return response

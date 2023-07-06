from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from ip import get_country_iso
from mongo import get_all_cloacking_codes
from uvicorn import run


def startup_message():
    print('Server has been started.')
    
    
app = FastAPI(on_startup=[startup_message])

templates = Jinja2Templates(directory="../templates")


def get_client_ip(request: Request) -> str:
    headers = request.headers
    forwarded = headers.get('X-Forwarded-For', '')
    if forwarded:
        return forwarded.split(',')[0]
    return request.client.host


def validate_iso(iso: str):
    return iso == 'UA'


def error_page(request: Request):
    return templates.TemplateResponse('error.html', {"request": request})


@app.get("/")
async def nothing(request: Request):
    return error_page(request=request)


@app.get("/{code}")
async def root(code: str, request: Request):
    client_ip = get_client_ip(request=request)
    try:
        iso_code = get_country_iso(ip=client_ip)
    except:
        return error_page(request=request)
    
    codes = get_all_cloacking_codes()
    if  code not in codes:
        return error_page(request=request)
    
    return RedirectResponse(codes.get(code))
    

def run_server(host='0.0.0.0', port=80):
    run(app, host=host, port=port)
    
    
if __name__ == "__main__":
    run_server()
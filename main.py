from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/health/', summary='HealthCheck EndPoint', tags=['Health Check'])
def healthcheck():
    return {'status': 'OK'}

# if __name__ == '__main__':
#     uvicorn.run('main:app', port=8000, reload=True)
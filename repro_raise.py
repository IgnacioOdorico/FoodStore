from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app, raise_server_exceptions=True)
resp = client.post('/api/v1/auth/token', data={'username':'empleado@nachopizza.com','password':'Empleado1234!'})
print('login', resp.status_code, resp.text)
resp = client.get('/api/v1/categorias/')
print('categorias status', resp.status_code)
print(resp.text)

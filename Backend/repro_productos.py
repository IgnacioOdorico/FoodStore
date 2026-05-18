from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app, raise_server_exceptions=True)

# Login
resp = client.post('/api/v1/auth/token', data={'username':'empleado@nachopizza.com','password':'Empleado1234!'})
print('login', resp.status_code, resp.text)

# Request productos
resp = client.get('/productos/')
print('productos status', resp.status_code)
print(resp.text)

# Request specific product 1
resp = client.get('/productos/1')
print('producto 1 status', resp.status_code)
print(resp.text)

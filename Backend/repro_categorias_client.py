from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Login
resp = client.post('/api/v1/auth/token', data={'username': 'empleado@nachopizza.com', 'password': 'Empleado1234!'})
print('login', resp.status_code, resp.text)

# Get categorias
resp = client.get('/api/v1/categorias/')
print('categorias', resp.status_code)
try:
    print(resp.json())
except Exception as e:
    print('json error', e)


from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Login
resp = client.post('/api/v1/auth/token', data={'username': 'empleado@nachopizza.com', 'password': 'Empleado1234!'})
print('login', resp.status_code)
token = resp.json().get('access_token')

headers = {"Authorization": f"Bearer {token}"}

# Get categorias
resp = client.get('/api/v1/categorias/', headers=headers)
print('categorias status', resp.status_code)
try:
    data = resp.json()
    print(f'categorias count: {len(data)}')
    if len(data) > 0:
        print(f'First category: {data[0]}')
except Exception as e:
    print('json error', e)


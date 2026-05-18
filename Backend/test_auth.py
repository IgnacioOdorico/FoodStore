import requests

login_url = "http://localhost:8000/api/v1/auth/token"
categorias_url = "http://localhost:8000/api/v1/categorias/"
me_url = "http://localhost:8000/api/v1/auth/me"

# OAuth2PasswordRequestForm uses form-data
payload = {
    "username": "empleado@nachopizza.com",
    "password": "Empleado1234!"
}

session = requests.Session()

try:
    print("Attempting login (form-data)...")
    login_resp = session.post(login_url, data=payload)
    print(f"Login Status: {login_resp.status_code}")
    print(f"Login Body: {login_resp.text}")
    
    print("\nGET Categorias:")
    cat_resp = session.get(categorias_url)
    print(f"Status: {cat_resp.status_code}")
    print(f"Body: {cat_resp.text}")

    print("\nGET Auth Me:")
    me_resp = session.get(me_url)
    print(f"Status: {me_resp.status_code}")
    print(f"Body: {me_resp.text}")

except Exception as e:
    print(f"Error: {e}")

import requests
import json

# Base URL for the API
BASE_URL = 'http://127.0.0.1:8000/api'

# Test login
login_data = {
    'username': 'testvendor2',
    'password': '0PDk2RbAKYe1'
}

# Create a session to persist cookies
session = requests.Session()

# Login
login_response = session.post(f'{BASE_URL}/login/', json=login_data)
print("Login Response:", login_response.status_code)
print("Login Data:", login_response.json())

if login_response.status_code == 200:
    # Access dashboard
    dashboard_response = session.get(f'{BASE_URL}/dashboard/')
    print("\nDashboard Response:", dashboard_response.status_code)
    print("Dashboard Data:", dashboard_response.json())
    
    # Try to create a product
    product_data = {
        'title': 'Test Product',
        'description': 'A test product',
        'price': 19.99,
        'stock': 10,
        'boutique': 1  # This should be handled automatically
    }
    
    product_response = session.post(f'{BASE_URL}/products/', json=product_data)
    print("\nProduct Creation Response:", product_response.status_code)
    print("Product Creation Data:", product_response.json())
    
    # Get products
    products_response = session.get(f'{BASE_URL}/products/')
    print("\nProducts Response:", products_response.status_code)
    print("Products Data:", products_response.json())
else:
    print("Login failed!")
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

print("=== Testing Vendor Authentication System ===\n")

# 1. Test login
print("1. Testing login...")
login_response = session.post(f'{BASE_URL}/login/', json=login_data)
print(f"Login Response: {login_response.status_code}")
if login_response.status_code == 200:
    print("✓ Login successful")
    user_data = login_response.json()['user']
    print(f"  Logged in as: {user_data['username']}")
else:
    print("✗ Login failed")
    print(login_response.text)
    exit()

# 2. Test dashboard access
print("\n2. Testing dashboard access...")
dashboard_response = session.get(f'{BASE_URL}/dashboard/')
print(f"Dashboard Response: {dashboard_response.status_code}")
if dashboard_response.status_code == 200:
    print("✓ Dashboard access successful")
    dashboard_data = dashboard_response.json()
    print(f"  Boutique: {dashboard_data['name']}")
    print(f"  Owner: {dashboard_data['owner']['username']}")
else:
    print("✗ Dashboard access failed")
    print(dashboard_response.text)

# 3. Test getting products (should be empty initially)
print("\n3. Testing products list...")
products_response = session.get(f'{BASE_URL}/products/')
print(f"Products Response: {products_response.status_code}")
if products_response.status_code == 200:
    products_data = products_response.json()
    print(f"✓ Products list retrieved, count: {len(products_data['results'])}")
else:
    print("✗ Products list failed")
    print(products_response.text)

# 4. Test creating a category
print("\n4. Testing category creation...")
category_data = {
    'name': 'Electronics',
    'description': 'Electronic devices and accessories',
    'boutique': 2  # This should be handled automatically
}
category_response = session.post(f'{BASE_URL}/categories/', json=category_data)
print(f"Category Creation Response: {category_response.status_code}")
if category_response.status_code == 201:
    print("✓ Category created successfully")
    category_info = category_response.json()
    print(f"  Category ID: {category_info['id']}, Name: {category_info['name']}")
    category_id = category_info['id']
else:
    print("✗ Category creation failed")
    print(category_response.text)

# 5. Test creating a product
print("\n5. Testing product creation...")
product_data = {
    'title': 'Smartphone',
    'description': 'Latest model smartphone',
    'price': 699.99,
    'stock': 50,
    'categories': []  # Will be linked later if needed
}
product_response = session.post(f'{BASE_URL}/products/', json=product_data)
print(f"Product Creation Response: {product_response.status_code}")
if product_response.status_code == 201:
    print("✓ Product created successfully")
    product_info = product_response.json()
    print(f"  Product ID: {product_info['id']}, Title: {product_info['title']}")
    product_id = product_info['id']
else:
    print("✗ Product creation failed")
    print(product_response.text)

# 6. Test getting products again (should now have 1)
print("\n6. Testing products list after creation...")
products_response = session.get(f'{BASE_URL}/products/')
print(f"Products Response: {products_response.status_code}")
if products_response.status_code == 200:
    products_data = products_response.json()
    print(f"✓ Products list retrieved, count: {len(products_data['results'])}")
    if len(products_data['results']) > 0:
        print(f"  First product: {products_data['results'][0]['title']}")
else:
    print("✗ Products list failed")
    print(products_response.text)

# 7. Test getting categories
print("\n7. Testing categories list...")
categories_response = session.get(f'{BASE_URL}/categories/')
print(f"Categories Response: {categories_response.status_code}")
if categories_response.status_code == 200:
    categories_data = categories_response.json()
    # Check if it's paginated like products
    if 'results' in categories_data:
        print(f"✓ Categories list retrieved, count: {len(categories_data['results'])}")
        if len(categories_data['results']) > 0:
            print(f"  First category: {categories_data['results'][0]['name']}")
    else:
        print(f"✓ Categories list retrieved, count: {len(categories_data)}")
        if len(categories_data) > 0:
            print(f"  First category: {categories_data[0]['name']}")
else:
    print("✗ Categories list failed")
    print(categories_response.text)

# 8. Test logout
print("\n8. Testing logout...")
logout_response = session.post(f'{BASE_URL}/logout/')
print(f"Logout Response: {logout_response.status_code}")
if logout_response.status_code == 200:
    print("✓ Logout successful")
else:
    print("✗ Logout failed")
    print(logout_response.text)

print("\n=== Testing Completed ===")
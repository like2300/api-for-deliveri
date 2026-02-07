# Multi-Vendor Shop Authentication System

This project implements a multi-vendor shop authentication and management system with secure dashboards for vendors.

## Features

### Authentication System
- Custom `VendorUser` model extending Django's AbstractBaseUser
- Secure login/logout functionality
- Password change capability
- Session and token-based authentication

### Vendor Dashboard
- Each vendor has their own private dashboard
- Ability to manage their own products
- Ability to create, modify and delete product categories
- Product-category association
- Ability to manage product types
- Password change functionality

### Admin Management
- Admin can create vendor accounts
- Automatic generation of initial passwords
- Management of vendor accounts

### Security & Isolation
- Vendors can only access their own data
- Custom permissions to ensure data isolation
- Proper authentication and authorization checks

## Models

### VendorUser
- Custom user model for vendors
- Extends AbstractBaseUser and PermissionsMixin
- Links to a single Boutique

### Boutique
- Represents a vendor's store
- Linked to a single VendorUser
- Contains products and categories

### Category
- Product categories specific to each boutique
- Belongs to a single boutique

### Product
- Products belong to a specific boutique
- Can be associated with multiple categories

## API Endpoints

### Authentication
- `POST /api/login/` - Vendor login
- `POST /api/logout/` - Vendor logout
- `POST /api/change-password/` - Change password

### Vendor Dashboard
- `GET /api/dashboard/` - Get vendor dashboard data
- `GET /api/products/` - List vendor's products
- `POST /api/products/` - Create a product
- `GET /api/products/{id}/` - Retrieve a product
- `PUT /api/products/{id}/` - Update a product
- `DELETE /api/products/{id}/` - Delete a product
- `GET /api/categories/` - List vendor's categories
- `POST /api/categories/` - Create a category
- `GET /api/categories/{id}/` - Retrieve a category
- `PUT /api/categories/{id}/` - Update a category
- `DELETE /api/categories/{id}/` - Delete a category

### Public Endpoints
- `GET /api/init-app-data/` - Get all app data
- `GET /api/public/products/` - List all products
- `GET /api/public/boutiques/` - List all boutiques
- `GET /api/public/sliders/` - List all sliders
- `GET /api/public/config/` - Get company config

## Management Commands

### Creating Vendor Accounts
```bash
python manage.py create_vendor_account --username vendor1 --email vendor1@example.com --boutique-name "Vendor 1 Store" --description "Official store of Vendor 1"
```

This command:
- Creates a new vendor user account
- Generates a random initial password
- Creates a corresponding boutique
- Links the user to the boutique

## Security Measures

- Custom `IsVendorOwner` permission class ensures vendors can only access their own data
- Proper authentication checks on all protected endpoints
- Data isolation between different vendors
- Secure password handling

## Usage

1. Create a vendor account using the management command
2. Vendor logs in using their username and initial password
3. Vendor can access their dashboard to manage products and categories
4. Vendors can only see and modify their own data
5. Admin manages vendor accounts through Django admin

## Architecture Notes

- Uses Django REST Framework for API endpoints
- Custom user model with proper relationship to boutiques
- Proper separation between public and private endpoints
- Comprehensive serialization of data
- Proper error handling and validation
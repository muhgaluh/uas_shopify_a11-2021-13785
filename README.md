
# Capstone Project UAS Pemrograman Sisi Server
## Shopify Backend Customer, Customer Address, Product, Product Variant

Muh Galuh Surya Putra Kusuma (A11.2021.13785/A11.4601)
----------

## Instalasi Aplikasi


Clone repository

    git clone https://github.com/muhgaluh/uas_shopify_a11-2021-13785.git

Build dan run container

    docker-compose up -d --build

Migrasi basis data

    docker-compose exec django python manage.py makemigrations 
    docker-compose exec django python manage.py migrate

Import dummy data

    docker-compose exec django python importer.py

----------

# Panduan Menjalankan Endpoint
urls insomnia: http://localhost:8002/admin/api/2024-07/
## Customer
- Get All Customers (customers.json)
- Get Single Customers (customers/id_cust.json)
- Get Count Customers (customers/count.json)
- Get Search Customer (customers/count.json) dengan params query first name, last name, atau email
- Post Add Customer (customers.json)
- Put Update Customer (customers/id_cust.json)
- Delete Customer (customers/id_cust.json)
## Customer Address
- Get All Address (customers.json)
- Get Single Address (customers/id_cust.json)
- Post Add Address (customers/id_cust/addresses.json)
- Put Set Default Address (customers/id_cust/addresses/id_addr/default.json)
- Put Update Address (customers/id_cust/addresses/id_addr.json)
- Delete Address (customers/id_cust/addresses/id_addr.json)
## Product
- Get All Products (products.json)
- Get Count Products (products/count.json)
- Post Add Product (products.json)
- Delete Product (product/product_id.json)
## Product Variant
- Get All Products Variant (products.json)
- Post Add Product Variant (products/id_prod/variants.json)
- Delete Product Variant (product/id_prod/variants/id_var.json)





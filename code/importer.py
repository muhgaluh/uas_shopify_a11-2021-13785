import os
import sys
import json
sys.path.append(os.path.abspath(os.path.join(__file__, *[os.pardir] * 3)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'shopif.settings'
import django
django.setup()

from customer.models import User, Customer, Address
from product.models import Product, ProductVariant

filepath = './dummy-data/'

with open(filepath+'customer.json') as jsonfile:
    customers = json.load(jsonfile)
    for cust in customers:
        existUser = User.objects.filter(email=cust['email']).first()
        if existUser == None:
            user = User.objects.create_user(username=cust['email'], email=cust['email'],
                                           password=cust['password'], first_name=cust['first_name'],
                                           last_name=cust['last_name'])
            
            existCust = Customer.objects.filter(user=user).first()
            if existCust == None:
                Customer.objects.create(user=user, created_at=cust['created_at'],
                                        updated_at=cust['created_at'], state=cust['state'],
                                        verified_email=cust['verified_email'],
                                        send_email_welcome=cust['send_email_welcome'],
                                        currency=cust['currency'],
                                        phone=cust['phone'])

with open(filepath + 'address.json') as jsonfile:
    addresses = json.load(jsonfile)
    for adr in addresses:
        customer_id = adr['customer']
        customer = Customer.objects.filter(id=customer_id).first()
        
        if customer is None:
            print(f"Pelanggan dengan id {customer_id} tidak ada. Melewati alamat ini.")
            continue
        
        addrExist = Address.objects.filter(customer_id=customer_id, address1=adr['address1']).first()
        if addrExist is None:
            Address.objects.create(
                customer=customer,
                address1=adr['address1'],
                address2=adr['address2'],
                city=adr['city'],
                province=adr['province'],
                country=adr['country'],
                company=adr['company'],
                phone=adr['phone'],
                zip=adr['zip'],
                default=adr['default']
            )

with open(filepath+'product.json') as jsonfile:
    products = json.load(jsonfile)
    for prod in products:
        existProd = Product.objects.filter(id=prod['id']).first()
        if existProd is None:
            Product.objects.create(
                id=prod['id'],
                title=prod['title'],
                handle=prod['handle'],
                product_type=prod['product_type'],
                status=prod['status'],
                tags=prod['tags'],
                vendor=prod['vendor'],
                created_at=prod['created_at'],
                updated_at=prod['updated_at']
            )

with open(filepath+'product_variant.json') as jsonfile:
    variants = json.load(jsonfile)
    for var in variants:
        product = Product.objects.filter(id=var['product_id']).first()
        if product:
            existVariant = ProductVariant.objects.filter(id=var['id']).first()
            if existVariant is None:
                ProductVariant.objects.create(
                    id=var['id'],
                    product=product,
                    title=var['title'],
                    sku=var['sku'],
                    price=var['price'],
                    inventory_quantity=var['inventory_quantity'],
                    weight=var['weight'],
                    weight_unit=var['weight_unit'],
                    created_at=var['created_at'],
                    updated_at=var['updated_at']
                )
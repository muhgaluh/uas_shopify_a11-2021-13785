from typing import List
from ninja import NinjaAPI, Query
from django.db.models import Q

from ninja_simple_jwt.auth.views.api import mobile_auth_router
from ninja_simple_jwt.auth.ninja_auth import HttpJwtAuth

from .models import User, Customer, Address
#Product, ProductVariant

from .schemas import CustomerOut, CustomerResp, AddressIn, AddressResp, SingleCustomerResp, AllAddrResp, CustomerIn, CustomerUpdate, AddressUpdate
#ProductOut, ProductVariantOut, ProductResp, ProductVariantResp

api = NinjaAPI()
api.add_router("/auth/", mobile_auth_router)
apiAuth = HttpJwtAuth()

@api.get("hello")
def helloWorld(request):
    return{'hello':'world'}

@api.get('customers/count.json', auth=apiAuth)
def getCountCustomer(request):
    customer_count = Customer.objects.count()
    return {"count customer": customer_count}

@api.get("customers/search.json", auth=apiAuth, response=CustomerResp)
def searchCustomers(request, query: str):
    customers = Customer.objects.filter(
        Q(user__first_name=query) |
        Q(user__last_name=query) |
        Q(user__email=query)
    ).distinct()
    return {'customers': customers}

@api.get("customers.json", auth=apiAuth, response=CustomerResp)
def getAllCustomers(request, ids:str):
    int_ids = ids.split(',')
    customers = Customer.objects.filter(id__in=int_ids)
    return {'customers': customers}

@api.get("customers/{id_cust}.json", auth=apiAuth, response=SingleCustomerResp)
def getSingleCustomer(request, id_cust: int):
    customer = Customer.objects.get(id=id_cust)
    return {'customer': customer}


@api.get("customers/{id_cust}/addresses.json", auth=apiAuth, response=AllAddrResp)
def getAllAddresses(request, id_cust: int):
    addresses = Address.objects.filter(customer_id=id_cust)
    return {"customers_address": addresses}

@api.get("customers/{id_cust}/addresses/{id_addr}.json", auth=apiAuth, response=AddressResp)
def getSingleAddress(request, id_cust: int, id_addr: int):
    address = Address.objects.get(pk=id_addr, customer_id=id_cust)
    return {"customer_address": address}

@api.post('customers.json', auth=apiAuth, response=SingleCustomerResp)
def addCustomer(request, data: CustomerIn):
    user = User.objects.create_user(
        username=data.email,
        email=data.email,
        password=data.password,
        first_name=data.first_name,
        last_name=data.last_name
    )
    
    customer = Customer.objects.create(
        user=user,
        phone=data.phone,
        verified_email=data.verified_email,
        send_email_welcome=data.send_email_welcome,
        state=data.state,
        currency=data.currency
    )

    return {"customer": customer}

@api.post('customers/{id_cust}/addresses.json', auth=apiAuth, response=AddressResp)
def addCustomer(request, id_cust:int, data:AddressIn):
    cust = Customer.objects.get(pk=id_cust)
    newAddr = Address.objects.create(
                customer=cust,
                address1=data.address1,
                address2=data.address2,
                city=data.city,
                province=data.province,
                company=data.company,
                phone=data.phone,
                zip=data.zip
            )
    return {"customer_address": newAddr}

@api.put('customers/{id_cust}.json', auth=apiAuth, response=SingleCustomerResp)
def updateCustomer(request, id_cust: int, data: CustomerUpdate):
    try:
        customer = Customer.objects.get(pk=id_cust)
        user = customer.user
        
        if data.email:
            user.email = data.email
            user.username = data.email
        
        if data.password:
            user.set_password(data.password)
        
        if data.first_name:
            user.first_name = data.first_name
        
        if data.last_name:
            user.last_name = data.last_name
        
        user.save()

        if data.phone:
            customer.phone = data.phone
        
        if data.verified_email is not None:
            customer.verified_email = data.verified_email
        
        if data.send_email_welcome is not None:
            customer.send_email_welcome = data.send_email_welcome
        
        if data.state:
            customer.state = data.state
        
        if data.currency:
            customer.currency = data.currency

        customer.save()
        return {"customer": customer}
    except Customer.DoesNotExist:
        raise HttpError(404, "Customer not found")
    
@api.put('customers/{id_cust}/addresses/{id_addr}.json', auth=apiAuth, response=AddressResp)
def updateAddress(request, id_cust: int, id_addr: int, data: AddressUpdate):
    try:
        address = Address.objects.get(pk=id_addr, customer_id=id_cust)

        if data.address1:
            address.address1 = data.address1
        
        if data.address2:
            address.address2 = data.address2
        
        if data.city:
            address.city = data.city
        
        if data.province:
            address.province = data.province
        
        if data.country:
            address.country = data.country
        
        if data.zip:
            address.zip = data.zip
        
        if data.phone:
            address.phone = data.phone
        
        if data.company:
            address.company = data.company
        
        if data.default is not None:
            address.default = data.default
        
        address.save()

        return {"customer_address": address}
    except Address.DoesNotExist:
        raise HttpError(404, "Address not found")

@api.put('customers/{id_cust}/addresses/{id_addr}/default.json', auth=apiAuth, response=AddressResp)
def setDefaultAddr(request, id_cust:int, id_addr:int):
    addr = Address.objects.get(pk=id_addr)
    addr.default =True
    addr.save()
    other = Address.objects.filter(customer_id=id_cust).exclude(id=id_addr)
    for data in other:
        data.default = False
        data.save()

    return {"customer_address": addr}

@api.delete('customers/{id_cust}/addresses/{id_addr}.json')
def deleteAddr(request, id_cust:int, id_addr:int):
    Address.objects.get(pk=id_addr).delete()
    return {}

@api.delete('customers/{id_cust}.json')
def deleteCust(request, id_cust:int):
    Customer.objects.get(pk=id_cust).delete()
    return {}

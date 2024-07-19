from ninja import Router, Query
from django.db.models import Q
from .models import Product, ProductVariant
from .schemas import ProductIn, ProductOut, ProductVariantIn, ProductVariantOut, AllProdResp, AllVarResp
from ninja_simple_jwt.auth.ninja_auth import HttpJwtAuth

product_router = Router()
apiAuth = HttpJwtAuth()

@product_router.get("bello")
def helloWorld(request):
    return{'bello':'world'}

@product_router.get('products/count.json', auth=apiAuth)
def getCountProduct(request):
    product_count = Product.objects.count()
    return {"count product": product_count}

@product_router.get('products.json', auth=apiAuth, response=AllProdResp)
def getAllProduct(request):
    products = Product.objects.all().prefetch_related('productvariant_set')
    product_out_list = []
    for product in products:
        variants = ProductVariant.objects.filter(product=product)
        product_out = ProductOut(
            id=product.id,
            title=product.title,
            handle=product.handle,
            product_type=product.product_type,
            status=product.status,
            tags=product.tags,
            vendor=product.vendor,
            created_at=product.created_at,
            updated_at=product.updated_at,
            variants=[ProductVariantOut.from_orm(variant) for variant in variants]
        )
        product_out_list.append(product_out)
    return {"products": product_out_list}


@product_router.get('products/{product_id}/variants.json', auth=apiAuth, response=AllVarResp)
def getAllProductVariants(request, product_id: int):
    variants = ProductVariant.objects.filter(product_id=product_id)
    variant_out_list = [ProductVariantOut.from_orm(variant) for variant in variants]
    return {"products": variant_out_list}

@product_router.post('products.json', response=ProductIn)
def add_product(request, product_in: ProductIn):
    product = Product.objects.create(**product_in.dict())
    return product_in

@product_router.post('products/{product_id}/variants.json', response=ProductVariantIn)
def add_product_variant(request, product_id: int, variant_in: ProductVariantIn):
    product = Product.objects.get(id=product_id)
    variant = ProductVariant.objects.create(product=product, **variant_in.dict())
    return variant_in

@product_router.delete('products/{id_prod}/variants/{id_var}.json')
def deleteAddr(request, id_prod:int, id_var:int):
    ProductVariant.objects.get(pk=id_var).delete()
    return {}

@product_router.delete('products/{id_prod}.json')
def deleteCust(request, id_prod:int):
    Product.objects.get(pk=id_prod).delete()
    return {}

from ninja import Schema, ModelSchema, FilterSchema, Field
from datetime import datetime
from typing import Optional, List, Self
from pydantic import model_validator

from product.models import Product, ProductVariant

class ProductVariantIn(Schema):
    product_id: int
    title: str
    sku: str
    price: float
    inventory_quantity: int
    weight: float
    weight_unit: str

class ProductVariantOut(Schema):
    id: int
    product_id: int
    title: str
    sku: str
    price: float
    inventory_quantity: int
    weight: float
    weight_unit: str
    created_at: datetime
    updated_at: datetime

class AllVarResp(Schema):
    products: List[ProductVariantOut]

class ProductIn(Schema):
    title: str
    handle: str
    product_type: str
    status: str = 'active'
    tags: str = ''
    vendor: str

class ProductOut(Schema):
    id: int
    title: str
    handle: str
    product_type: str
    status: str
    tags: str
    vendor: str
    created_at: datetime
    updated_at: datetime
    variants: Optional[List[ProductVariantOut]] = Field(alias='variants')

class AllProdResp(Schema):
    products: List[ProductOut]


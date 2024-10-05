import pytest

from core.apps.products.services.products import (
    BaseProductService,
    OrmProductService,
)


@pytest.fixture
def product_service() -> BaseProductService:
    return OrmProductService()

from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime

from core.apps.common.enums import EntityStatus
from core.apps.customers.entities.customers import CustomerEntity
from core.apps.products.entities.products import Product as ProductEntity


@dataclass
class Review:
    id: int | None = field(default=None, kw_only=True)  # noqa
    customer: CustomerEntity | EntityStatus = field(
        default=EntityStatus.NOT_LOADED,
    )
    product: ProductEntity | EntityStatus = field(
        default=EntityStatus.NOT_LOADED,
    )
    rating: int = field(default=1)
    text: str = field(default='')
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime | None = field(default=None)

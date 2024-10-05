from dataclasses import dataclass

from ninja import Schema


@dataclass(frozen=True)
class ProductFilters(Schema):
    search: str | None = None

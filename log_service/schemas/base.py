"""Base schemas"""

from typing import Generic, List, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response schema"""

    items: List[T]
    total: int
    page: int
    page_size: int


class DetailResponse(BaseModel, Generic[T]):
    """Detail response schema"""

    data: T

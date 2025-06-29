"""Pagination"""

from typing import List, TypeVar

from schemas.base import DetailResponse, PaginatedResponse

T = TypeVar("T")


def create_paginated_response(
    items: List[T], total: int, page: int, size: int
) -> PaginatedResponse[T]:
    """Create a paginated response"""

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=size,
    )


def create_detail_response(data: T) -> DetailResponse[T]:
    """Create a detail response"""
    return DetailResponse(data=data)

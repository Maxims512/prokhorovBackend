from fastapi import APIRouter, HTTPException, status

from project.infrastructure.postgres.database import PostgresDatabase
from project.infrastructure.postgres.repository.discount_repo import DiscountRepository
from project.schemas.discount import DiscountSchema, DiscountCreateUpdateSchema

from project.core.exceptions import DiscountNotFound

database = PostgresDatabase()
discount_router = APIRouter()


@discount_router.get(
    "/all_discounts",
    response_model=list[DiscountSchema],
    status_code=status.HTTP_200_OK
)
async def get_all_discounts() -> list[DiscountSchema]:
    async with database.session() as session:
        all_discounts = await DiscountRepository().get_all_discounts(session=session)

    return all_discounts


@discount_router.get(
    "/discount/{discount_id}",
    response_model=DiscountSchema,
    status_code=status.HTTP_200_OK
)
async def get_discount_by_id(
        discount_id: int,
) -> DiscountSchema:
    try:
        async with database.session() as session:
            discount = await DiscountRepository().get_discount_by_id(session=session, discount_id=discount_id)
    except DiscountNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return discount


@discount_router.post(
    "/add_discount",
    response_model=DiscountSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_discount(
        discount_dto: DiscountCreateUpdateSchema,
) -> DiscountSchema:
    async with database.session() as session:
        new_discount = await DiscountRepository().create_discount(session=session, discount=discount_dto)

    return new_discount


@discount_router.put(
    "/update_discount/{discount_id}",
    response_model=DiscountSchema,
    status_code=status.HTTP_200_OK,
)
async def update_discount(
        discount_id: int,
        discount_dto: DiscountCreateUpdateSchema,
) -> DiscountSchema:
    try:
        async with database.session() as session:
            updated_discount = await DiscountRepository().update_discount(
                session=session,
                discount_id=discount_id,
                discount=discount_dto,
            )
    except DiscountNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_discount


@discount_router.delete(
    "/delete_discount/{discount_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_discount(
        discount_id: int,
) -> None:
    try:
        async with database.session() as session:
            discount = await DiscountRepository().delete_discount(session=session, discount_id=discount_id)
    except DiscountNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return discount

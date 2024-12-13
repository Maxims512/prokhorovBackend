from fastapi import APIRouter, HTTPException, status

from project.infrastructure.postgres.database import PostgresDatabase
from project.infrastructure.postgres.repository.city_repo import CityRepository
from project.schemas.city import CitySchema, CityCreateUpdateSchema

from project.core.exceptions import CityNotFound

database = PostgresDatabase()
city_router = APIRouter()


@city_router.get(
    "/all_cities",
    response_model=list[CitySchema],
    status_code=status.HTTP_200_OK
)
async def get_all_cities() -> list[CitySchema]:
    async with database.session() as session:
        all_cities = await CityRepository().get_all_cities(session=session)

    return all_cities


@city_router.get(
    "/city/{city_id}",
    response_model=CitySchema,
    status_code=status.HTTP_200_OK
)
async def get_city_by_id(
        city_id: int,
) -> CitySchema:
    try:
        async with database.session() as session:
            city = await CityRepository().get_city_by_id(session=session, city_id=city_id)
    except CityNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return city


@city_router.post(
    "/add_city",
    response_model=CitySchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_city(
        city_dto: CityCreateUpdateSchema,
) -> CitySchema:
    async with database.session() as session:
        new_city = await CityRepository().create_city(session=session, city=city_dto)

    return new_city


@city_router.put(
    "/update_city/{city_id}",
    response_model=CitySchema,
    status_code=status.HTTP_200_OK,
)
async def update_city(
        city_id: int,
        city_dto: CityCreateUpdateSchema,
) -> CitySchema:
    try:
        async with database.session() as session:
            updated_city = await CityRepository().update_city(
                session=session,
                city_id=city_id,
                city=city_dto,
            )
    except CityNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_city


@city_router.delete(
    "/delete_city/{city_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_city(
        city_id: int,
) -> None:
    try:
        async with database.session() as session:
            city = await CityRepository().delete_city(session=session, city_id=city_id)
    except CityNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return city

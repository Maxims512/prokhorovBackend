from fastapi import APIRouter, HTTPException, status

from project.infrastructure.postgres.database import PostgresDatabase
from project.infrastructure.postgres.repository.airport_repo import AirportRepository
from project.schemas.airport import AirportSchema, AirportCreateUpdateSchema

from project.core.exceptions import AirportNotFound

database = PostgresDatabase()
airport_router = APIRouter()


@airport_router.get(
    "/all_airports",
    response_model=list[AirportSchema],
    status_code=status.HTTP_200_OK
)
async def get_all_airports() -> list[AirportSchema]:
    async with database.session() as session:
        all_airports = await AirportRepository().get_all_airports(session=session)

    return all_airports


@airport_router.get(
    "/airport/{airport_id}",
    response_model=AirportSchema,
    status_code=status.HTTP_200_OK
)
async def get_airport_by_id(
        airport_id: int,
) -> AirportSchema:
    try:
        async with database.session() as session:
            airport = await AirportRepository().get_airport_by_id(session=session, airport_id=airport_id)
    except AirportNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return airport


@airport_router.post(
    "/add_airport",
    response_model=AirportSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_airport(
        airport_dto: AirportCreateUpdateSchema,
) -> AirportSchema:
    async with database.session() as session:
        new_airport = await AirportRepository().create_airport(session=session, airport=airport_dto)

    return new_airport


@airport_router.put(
    "/update_airport/{airport_id}",
    response_model=AirportSchema,
    status_code=status.HTTP_200_OK,
)
async def update_airport(
        airport_id: int,
        airport_dto: AirportCreateUpdateSchema,
) -> AirportSchema:
    try:
        async with database.session() as session:
            updated_airport = await AirportRepository().update_airport(
                session=session,
                airport_id=airport_id,
                airport=airport_dto,
            )
    except AirportNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_airport


@airport_router.delete(
    "/delete_airport/{airport_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_airport(
        airport_id: int,
) -> None:
    try:
        async with database.session() as session:
            airport = await AirportRepository().delete_airport(session=session, airport_id=airport_id)
    except AirportNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return airport

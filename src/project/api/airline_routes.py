from fastapi import APIRouter, HTTPException, status

from project.infrastructure.postgres.database import PostgresDatabase
from project.infrastructure.postgres.repository.airline_repo import AirlineRepository
from project.schemas.airline import AirlineSchema, AirlineCreateUpdateSchema

from project.core.exceptions import AirlineNotFound

database = PostgresDatabase()
airline_router = APIRouter()


@airline_router.get(
    "/all_airlines",
    response_model=list[AirlineSchema],
    status_code=status.HTTP_200_OK
)
async def get_all_airlines() -> list[AirlineSchema]:
    async with database.session() as session:
        all_airlines = await AirlineRepository().get_all_airlines(session=session)

    return all_airlines


@airline_router.get(
    "/airline/{airline_id}",
    response_model=AirlineSchema,
    status_code=status.HTTP_200_OK
)
async def get_airline_by_id(
        airline_id: int,
) -> AirlineSchema:
    try:
        async with database.session() as session:
            airline = await AirlineRepository().get_airline_by_id(session=session, airline_id=airline_id)
    except AirlineNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return airline


@airline_router.post(
    "/add_airline",
    response_model=AirlineSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_airline(
        airline_dto: AirlineCreateUpdateSchema,
) -> AirlineSchema:
    async with database.session() as session:
        new_airline = await AirlineRepository().create_airline(session=session, airline=airline_dto)

    return new_airline


@airline_router.put(
    "/update_airline/{airline_id}",
    response_model=AirlineSchema,
    status_code=status.HTTP_200_OK,
)
async def update_airline(
        airline_id: int,
        airline_dto: AirlineCreateUpdateSchema,
) -> AirlineSchema:
    try:
        async with database.session() as session:
            updated_airline = await AirlineRepository().update_airline(
                session=session,
                airline_id=airline_id,
                airline=airline_dto,
            )
    except AirlineNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_airline


@airline_router.delete(
    "/delete_airline/{airline_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_airline(
        airline_id: int,
) -> None:
    try:
        async with database.session() as session:
            airport = await AirlineRepository().delete_airline(session=session, airline_id=airline_id)
    except AirlineNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return airport

from fastapi import APIRouter, HTTPException, status

from project.infrastructure.postgres.database import PostgresDatabase
from project.infrastructure.postgres.repository.flight_repo import FlightRepository
from project.schemas.flight import FlightSchema, FlightCreateUpdateSchema

from project.core.exceptions import FlightNotFound

database = PostgresDatabase()
flight_router = APIRouter()


@flight_router.get(
    "/all_flights",
    response_model=list[FlightSchema],
    status_code=status.HTTP_200_OK
)
async def get_all_flights() -> list[FlightSchema]:
    async with database.session() as session:
        all_flights = await FlightRepository().get_all_flights(session=session)

    return all_flights


@flight_router.get(
    "/flight/{flight_id}",
    response_model=FlightSchema,
    status_code=status.HTTP_200_OK
)
async def get_flight_by_id(
        flight_id: int,
) -> FlightSchema:
    try:
        async with database.session() as session:
            flight = await FlightRepository().get_flight_by_id(session=session, flight_id=flight_id)
    except FlightNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return flight


@flight_router.post(
    "/add_flight",
    response_model=FlightSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_flight(
        flight_dto: FlightCreateUpdateSchema,
) -> FlightSchema:
    async with database.session() as session:
        new_flight = await FlightRepository().create_flight(session=session, flight=flight_dto)

    return new_flight


@flight_router.put(
    "/update_flight/{flight_id}",
    response_model=FlightSchema,
    status_code=status.HTTP_200_OK,
)
async def update_flight(
        flight_id: int,
        flight_dto: FlightCreateUpdateSchema,
) -> FlightSchema:
    try:
        async with database.session() as session:
            updated_flight = await FlightRepository().update_flight(
                session=session,
                flight_id=flight_id,
                flight=flight_dto,
            )
    except FlightNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_flight


@flight_router.delete(
    "/delete_flight/{flight_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_flight(
        flight_id: int,
) -> None:
    try:
        async with database.session() as session:
            flight = await FlightRepository().delete_flight(session=session, flight_id=flight_id)
    except FlightNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return flight

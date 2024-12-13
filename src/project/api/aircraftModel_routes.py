from fastapi import APIRouter, HTTPException, status

from project.infrastructure.postgres.database import PostgresDatabase
from project.infrastructure.postgres.repository.aircraftModel_repo import AircraftModelRepository
from project.schemas.aircraftModel import AircraftModelSchema, AircraftModelCreateUpdateSchema

from project.core.exceptions import AircraftModelNotFound

database = PostgresDatabase()
aircraft_model_router = APIRouter()


@aircraft_model_router.get(
    "/all_aircraft_models",
    response_model=list[AircraftModelSchema],
    status_code=status.HTTP_200_OK
)
async def get_all_aircraft_models() -> list[AircraftModelSchema]:
    async with database.session() as session:
        all_aircraft_models = await AircraftModelRepository().get_all_aircraft_models(session=session)

    return all_aircraft_models


@aircraft_model_router.get(
    "/aircraft_model/{aircraft_model_id}",
    response_model=AircraftModelSchema,
    status_code=status.HTTP_200_OK
)
async def get_aircraft_model_by_id(
        aircraft_model_id: int,
) -> AircraftModelSchema:
    try:
        async with (database.session() as session):
            aircraft_model = await AircraftModelRepository().get_aircraft_model_by_id(session=session
                                                                                      , aircraft_model_id
                                                                                      =aircraft_model_id)
    except AircraftModelNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return aircraft_model


@aircraft_model_router.post(
    "/add_aircraft_model",
    response_model=AircraftModelSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_aircraft_model(
        aircraft_model_dto: AircraftModelCreateUpdateSchema,
) -> AircraftModelSchema:
    async with database.session() as session:
        new_aircraft_model = await AircraftModelRepository().create_aircraft_model(session=session
                                                                                   , aircraft_model=aircraft_model_dto)

    return new_aircraft_model


@aircraft_model_router.put(
    "/update_aircraft_model/{aircraft_model_id}",
    response_model=AircraftModelSchema,
    status_code=status.HTTP_200_OK,
)
async def update_aircraft_model(
        aircraft_model_id: int,
        aircraft_model_dto: AircraftModelCreateUpdateSchema,
) -> AircraftModelSchema:
    try:
        async with database.session() as session:
            updated_aircraft_model = await AircraftModelRepository().update_aircraft_model(
                session=session,
                aircraft_model_id=aircraft_model_id,
                aircraft_model=aircraft_model_dto,
            )
    except AircraftModelNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_aircraft_model


@aircraft_model_router.delete(
    "/delete_aircraftModel/{aircraftModel_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_aircraft_model(
        aircraft_model_id: int,
) -> None:
    try:
        async with database.session() as session:
            airport = await AircraftModelRepository().delete_aircraft_model(session=session
                                                                            , aircraft_model_id=aircraft_model_id)
    except AircraftModelNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return airport

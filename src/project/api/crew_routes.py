from fastapi import APIRouter, HTTPException, status

from project.infrastructure.postgres.database import PostgresDatabase
from project.infrastructure.postgres.repository.crew_repo import CrewRepository
from project.schemas.crew import CrewSchema, CrewCreateUpdateSchema

from project.core.exceptions import CrewNotFound

database = PostgresDatabase()
crew_router = APIRouter()


@crew_router.get(
    "/all_crews",
    response_model=list[CrewSchema],
    status_code=status.HTTP_200_OK
)
async def get_all_users() -> list[CrewSchema]:
    async with database.session() as session:
        all_crews = await CrewRepository().get_all_crews(session=session)

    return all_crews


@crew_router.get(
    "/crew/{crew_id}",
    response_model=CrewSchema,
    status_code=status.HTTP_200_OK
)
async def get_crew_by_id(
        crew_id: int,
) -> CrewSchema:
    try:
        async with database.session() as session:
            crew = await CrewRepository().get_crew_by_id(session=session, crew_id=crew_id)
    except CrewNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return crew


@crew_router.post(
    "/add_crew",
    response_model=CrewSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_crew(
        crew_dto: CrewCreateUpdateSchema,
) -> CrewSchema:
    async with database.session() as session:
        new_crew = await CrewRepository().create_crew(session=session, crew=crew_dto)

    return new_crew


@crew_router.put(
    "/update_crew/{crew_id}",
    response_model=CrewSchema,
    status_code=status.HTTP_200_OK,
)
async def update_crew(
        crew_id: int,
        crew_dto: CrewCreateUpdateSchema,
) -> CrewSchema:
    try:
        async with database.session() as session:
            updated_crew = await CrewRepository().update_crew(
                session=session,
                crew_id=crew_id,
                crew=crew_dto,
            )
    except CrewNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_crew


@crew_router.delete(
    "/delete_crew/{crew_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_crew(
        crew_id: int,
) -> None:
    try:
        async with database.session() as session:
            crew = await CrewRepository().delete_crew(session=session, crew_id=crew_id)
    except CrewNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return crew

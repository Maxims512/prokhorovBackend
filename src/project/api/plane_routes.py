from fastapi import APIRouter, HTTPException, status

from project.infrastructure.postgres.database import PostgresDatabase
from project.infrastructure.postgres.repository.plane_repo import PlaneRepository
from project.schemas.plane import PlaneSchema, PlaneCreateUpdateSchema

from project.core.exceptions import PlaneNotFound

database = PostgresDatabase()
plane_router = APIRouter()


@plane_router.get(
    "/all_planes",
    response_model=list[PlaneSchema],
    status_code=status.HTTP_200_OK
)
async def get_all_users() -> list[PlaneSchema]:
    async with database.session() as session:
        all_planes = await PlaneRepository().get_all_planes(session=session)

    return all_planes


@plane_router.get(
    "/plane/{plane_id}",
    response_model=PlaneSchema,
    status_code=status.HTTP_200_OK
)
async def get_plane_by_id(
        plane_id: int,
) -> PlaneSchema:
    try:
        async with database.session() as session:
            plane = await PlaneRepository().get_plane_by_id(session=session, plane_id=plane_id)
    except PlaneNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return plane


@plane_router.post(
    "/add_plane",
    response_model=PlaneSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_plane(
        plane_dto: PlaneCreateUpdateSchema,
) -> PlaneSchema:
    async with database.session() as session:
        new_plane = await PlaneRepository().create_plane(session=session, plane=plane_dto)

    return new_plane


@plane_router.put(
    "/update_plane/{plane_id}",
    response_model=PlaneSchema,
    status_code=status.HTTP_200_OK,
)
async def update_plane(
        plane_id: int,
        plane_dto: PlaneCreateUpdateSchema,
) -> PlaneSchema:
    try:
        async with database.session() as session:
            updated_plane = await PlaneRepository().update_plane(
                session=session,
                plane_id=plane_id,
                plane=plane_dto,
            )
    except PlaneNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_plane


@plane_router.delete(
    "/delete_plane/{plane_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_plane(
        plane_id: int,
) -> None:
    try:
        async with database.session() as session:
            plane = await PlaneRepository().delete_plane(session=session, plane_id=plane_id)
    except PlaneNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return plane

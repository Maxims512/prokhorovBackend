from fastapi import APIRouter, HTTPException, status

from project.infrastructure.postgres.database import PostgresDatabase
from project.infrastructure.postgres.repository.route_repo import RouteRepository
from project.schemas.route import RouteSchema, RouteCreateUpdateSchema

from project.core.exceptions import RouteNotFound

database = PostgresDatabase()
route_router = APIRouter()


@route_router.get(
    "/all_routes",
    response_model=list[RouteSchema],
    status_code=status.HTTP_200_OK
)
async def get_all_users() -> list[RouteSchema]:
    async with database.session() as session:
        all_routes = await RouteRepository().get_all_routes(session=session)

    return all_routes


@route_router.get(
    "/route/{route_id}",
    response_model=RouteSchema,
    status_code=status.HTTP_200_OK
)
async def get_route_by_id(
        route_id: int,
) -> RouteSchema:
    try:
        async with database.session() as session:
            route = await RouteRepository().get_route_by_id(session=session, route_id=route_id)
    except RouteNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return route


@route_router.post(
    "/add_route",
    response_model=RouteSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_route(
        route_dto: RouteCreateUpdateSchema,
) -> RouteSchema:
    async with database.session() as session:
        new_route = await RouteRepository().create_route(session=session, route=route_dto)

    return new_route


@route_router.put(
    "/update_route/{route_id}",
    response_model=RouteSchema,
    status_code=status.HTTP_200_OK,
)
async def update_route(
        route_id: int,
        route_dto: RouteCreateUpdateSchema,
) -> RouteSchema:
    try:
        async with database.session() as session:
            updated_route = await RouteRepository().update_route(
                session=session,
                route_id=route_id,
                route=route_dto,
            )
    except RouteNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_route


@route_router.delete(
    "/delete_route/{route_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_route(
        route_id: int,
) -> None:
    try:
        async with database.session() as session:
            route = await RouteRepository().delete_route(session=session, route_id=route_id)
    except RouteNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return route

from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, true
from sqlalchemy.exc import InterfaceError

from project.schemas.route import RouteSchema, RouteCreateUpdateSchema
from project.infrastructure.postgres.models import Route

from project.core.exceptions import RouteNotFound


class RouteRepository:
    _collection: Type[Route] = Route

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = select(true())

        try:
            return await session.scalar(query)
        except (Exception, InterfaceError):
            return False

    async def get_route_by_id(
            self,
            session: AsyncSession,
            route_id: int,
    ) -> RouteSchema:
        query = (
            select(self._collection)
            .where(self._collection.route_id == route_id)
        )

        route = await session.scalar(query)

        if not route:
            raise RouteNotFound(_id=route_id)

        return RouteSchema.model_validate(obj=route)

    async def get_all_routes(
            self,
            session: AsyncSession,
    ) -> list[RouteSchema]:
        query = select(self._collection)

        cities = await session.scalars(query)

        return [RouteSchema.model_validate(obj=route) for route in cities.all()]

    async def create_route(
            self,
            session: AsyncSession,
            route: RouteCreateUpdateSchema,
    ) -> RouteSchema:
        query = (
            insert(self._collection)
            .values(route.model_dump())
            .returning(self._collection)
        )

        created_route = await session.scalar(query)
        await session.flush()

        return RouteSchema.model_validate(obj=created_route)

    async def update_route(
            self,
            session: AsyncSession,
            route_id: int,
            route: RouteCreateUpdateSchema,
    ) -> RouteSchema:
        query = (
            update(self._collection)
            .where(self._collection.route_id == route_id)
            .values(route.model_dump())
            .returning(self._collection)
        )

        updated_route = await session.scalar(query)

        if not updated_route:
            raise RouteNotFound(_id=route_id)

        return RouteSchema.model_validate(obj=updated_route)

    async def delete_route(
            self,
            session: AsyncSession,
            route_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.route_id == route_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise RouteNotFound(_id=route_id)

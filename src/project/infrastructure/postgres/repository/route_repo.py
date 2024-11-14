
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.schemas.route import RouteSchema
from project.infrastructure.postgres.models import Route

from project.core.config import settings


class RouteRepository:
    _collection: Type[Route] = Route

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def create_route(
        self,
        session: AsyncSession,
        route: RouteSchema,
    ) -> RouteSchema:
        columns = ", ".join(route.model_dump().keys())
        values_placeholders = ", ".join(f":{key}" for key in route.model_dump().keys())
        query = f"""
            INSERT INTO {settings.POSTGRES_SCHEMA}.routes ({columns})
            VALUES ({values_placeholders})
            RETURNING *;
        """

        result = await session.execute(text(query), route.model_dump())
        await session.commit()

        new_route = result.mappings().first()
        return RouteSchema.model_validate(obj=new_route)

    async def get_route_by_id(
        self,
        session: AsyncSession,
        id: int,
    ) -> RouteSchema:
        query = f"""
            SELECT * FROM {settings.POSTGRES_SCHEMA}.routes
            WHERE id = :id;
        """

        result = await session.execute(text(query), {'id': id})
        route = result.mappings().first()

        return RouteSchema.model_validate(obj=route) if route else None

    async def update_route(
        self,
        session: AsyncSession,
        id: int,
        route: RouteSchema,
    ) -> RouteSchema:
        set_clause = ", ".join(f"{key} = :{key}" for key in route.model_dump().keys())
        query = f"""
            UPDATE {settings.POSTGRES_SCHEMA}.routes
            SET {set_clause}
            WHERE id = :id
            RETURNING *;
        """

        params = route.model_dump()
        params['id'] = id

        result = await session.execute(text(query), params)
        await session.commit()

        updated_route = result.mappings().first()
        return RouteSchema.model_validate(obj=updated_route) if updated_route else None

    async def delete_route(
        self,
        session: AsyncSession,
        id: int,
    ) -> dict:
        query = f"""
            DELETE FROM {settings.POSTGRES_SCHEMA}.routes
            WHERE id = :id;
        """

        await session.execute(text(query), {'id': id})
        await session.commit()

        return {'status': 'success', 'message': 'Route deleted successfully'}

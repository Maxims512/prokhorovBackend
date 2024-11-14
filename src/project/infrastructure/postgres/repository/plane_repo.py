
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.schemas.plane import PlaneSchema
from project.infrastructure.postgres.models import Plane

from project.core.config import settings


class PlaneRepository:
    _collection: Type[Plane] = Plane

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def create_plane(
        self,
        session: AsyncSession,
        plane: PlaneSchema,
    ) -> PlaneSchema:
        columns = ", ".join(plane.model_dump().keys())
        values_placeholders = ", ".join(f":{key}" for key in plane.model_dump().keys())
        query = f"""
            INSERT INTO {settings.POSTGRES_SCHEMA}.planes ({columns})
            VALUES ({values_placeholders})
            RETURNING *;
        """

        result = await session.execute(text(query), plane.model_dump())
        await session.commit()

        new_plane = result.mappings().first()
        return PlaneSchema.model_validate(obj=new_plane)

    async def get_plane_by_id(
        self,
        session: AsyncSession,
        id: int,
    ) -> PlaneSchema:
        query = f"""
            SELECT * FROM {settings.POSTGRES_SCHEMA}.planes
            WHERE id = :id;
        """

        result = await session.execute(text(query), {'id': id})
        plane = result.mappings().first()

        return PlaneSchema.model_validate(obj=plane) if plane else None

    async def update_plane(
        self,
        session: AsyncSession,
        id: int,
        plane: PlaneSchema,
    ) -> PlaneSchema:
        set_clause = ", ".join(f"{key} = :{key}" for key in plane.model_dump().keys())
        query = f"""
            UPDATE {settings.POSTGRES_SCHEMA}.planes
            SET {set_clause}
            WHERE id = :id
            RETURNING *;
        """

        params = plane.model_dump()
        params['id'] = id

        result = await session.execute(text(query), params)
        await session.commit()

        updated_plane = result.mappings().first()
        return PlaneSchema.model_validate(obj=updated_plane) if updated_plane else None

    async def delete_plane(
        self,
        session: AsyncSession,
        id: int,
    ) -> dict:
        query = f"""
            DELETE FROM {settings.POSTGRES_SCHEMA}.planes
            WHERE id = :id;
        """

        await session.execute(text(query), {'id': id})
        await session.commit()

        return {'status': 'success', 'message': 'Plane deleted successfully'}


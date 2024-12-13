from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, true
from sqlalchemy.exc import InterfaceError

from project.schemas.plane import PlaneSchema, PlaneCreateUpdateSchema
from project.infrastructure.postgres.models import Plane

from project.core.exceptions import PlaneNotFound


class PlaneRepository:
    _collection: Type[Plane] = Plane

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = select(true())

        try:
            return await session.scalar(query)
        except (Exception, InterfaceError):
            return False

    async def get_plane_by_id(
            self,
            session: AsyncSession,
            plane_id: int,
    ) -> PlaneSchema:
        query = (
            select(self._collection)
            .where(self._collection.plane_id == plane_id)
        )

        plane = await session.scalar(query)

        if not plane:
            raise PlaneNotFound(_id=plane_id)

        return PlaneSchema.model_validate(obj=plane)

    async def get_all_planes(
            self,
            session: AsyncSession,
    ) -> list[PlaneSchema]:
        query = select(self._collection)

        cities = await session.scalars(query)

        return [PlaneSchema.model_validate(obj=plane) for plane in cities.all()]

    async def create_plane(
            self,
            session: AsyncSession,
            plane: PlaneCreateUpdateSchema,
    ) -> PlaneSchema:
        query = (
            insert(self._collection)
            .values(plane.model_dump())
            .returning(self._collection)
        )

        created_plane = await session.scalar(query)
        await session.flush()

        return PlaneSchema.model_validate(obj=created_plane)

    async def update_plane(
            self,
            session: AsyncSession,
            plane_id: int,
            plane: PlaneCreateUpdateSchema,
    ) -> PlaneSchema:
        query = (
            update(self._collection)
            .where(self._collection.plane_id == plane_id)
            .values(plane.model_dump())
            .returning(self._collection)
        )

        updated_plane = await session.scalar(query)

        if not updated_plane:
            raise PlaneNotFound(_id=plane_id)

        return PlaneSchema.model_validate(obj=updated_plane)

    async def delete_plane(
            self,
            session: AsyncSession,
            plane_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.plane_id == plane_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise PlaneNotFound(_id=plane_id)

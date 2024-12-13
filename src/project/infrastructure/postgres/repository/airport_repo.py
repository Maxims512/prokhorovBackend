from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, true
from sqlalchemy.exc import InterfaceError

from project.schemas.airport import AirportSchema, AirportCreateUpdateSchema
from project.infrastructure.postgres.models import Airport

from project.core.exceptions import AirportNotFound


class AirportRepository:
    _collection: Type[Airport] = Airport

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = select(true())

        try:
            return await session.scalar(query)
        except (Exception, InterfaceError):
            return False

    async def get_airport_by_id(
            self,
            session: AsyncSession,
            airport_id: int,
    ) -> AirportSchema:
        query = (
            select(self._collection)
            .where(self._collection.airport_id == airport_id)
        )

        airport = await session.scalar(query)

        if not airport:
            raise AirportNotFound(_id=airport_id)

        return AirportSchema.model_validate(obj=airport)

    async def get_all_airports(
            self,
            session: AsyncSession,
    ) -> list[AirportSchema]:
        query = select(self._collection)

        airports = await session.scalars(query)

        return [AirportSchema.model_validate(obj=airport) for airport in airports.all()]

    async def create_airport(
            self,
            session: AsyncSession,
            airport: AirportCreateUpdateSchema,
    ) -> AirportSchema:
        query = (
            insert(self._collection)
            .values(airport.model_dump())
            .returning(self._collection)
        )

        created_airport = await session.scalar(query)
        await session.flush()

        return AirportSchema.model_validate(obj=created_airport)

    async def update_airport(
            self,
            session: AsyncSession,
            airport_id: int,
            airport: AirportCreateUpdateSchema,
    ) -> AirportSchema:
        query = (
            update(self._collection)
            .where(self._collection.airport_id == airport_id)
            .values(airport.model_dump())
            .returning(self._collection)
        )

        updated_airport = await session.scalar(query)

        if not updated_airport:
            raise AirportNotFound(_id=airport_id)

        return AirportSchema.model_validate(obj=updated_airport)

    async def delete_airport(
            self,
            session: AsyncSession,
            airport_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.airport_id == airport_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise AirportNotFound(_id=airport_id)

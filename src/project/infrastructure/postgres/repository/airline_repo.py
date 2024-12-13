from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, true
from sqlalchemy.exc import InterfaceError

from project.schemas.airline import AirlineSchema, AirlineCreateUpdateSchema
from project.infrastructure.postgres.models import Airline

from project.core.exceptions import AirlineNotFound


class AirlineRepository:
    _collection: Type[Airline] = Airline

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = select(true())

        try:
            return await session.scalar(query)
        except (Exception, InterfaceError):
            return False

    async def get_airline_by_id(
            self,
            session: AsyncSession,
            airline_id: int,
    ) -> AirlineSchema:
        query = (
            select(self._collection)
            .where(self._collection.airline_id == airline_id)
        )

        airline = await session.scalar(query)

        if not airline:
            raise AirlineNotFound(_id=airline_id)

        return AirlineSchema.model_validate(obj=airline)

    async def get_all_airlines(
            self,
            session: AsyncSession,
    ) -> list[AirlineSchema]:
        query = select(self._collection)

        airlines = await session.scalars(query)

        return [AirlineSchema.model_validate(obj=airline) for airline in airlines.all()]

    async def create_airline(
            self,
            session: AsyncSession,
            airline: AirlineCreateUpdateSchema,
    ) -> AirlineSchema:
        query = (
            insert(self._collection)
            .values(airline.model_dump())
            .returning(self._collection)
        )

        created_airline = await session.scalar(query)
        await session.flush()

        return AirlineSchema.model_validate(obj=created_airline)

    async def update_airline(
            self,
            session: AsyncSession,
            airline_id: int,
            airline: AirlineCreateUpdateSchema,
    ) -> AirlineSchema:
        query = (
            update(self._collection)
            .where(self._collection.airline_id == airline_id)
            .values(airline.model_dump())
            .returning(self._collection)
        )

        updated_airline = await session.scalar(query)

        if not updated_airline:
            raise AirlineNotFound(_id=airline_id)

        return AirlineSchema.model_validate(obj=updated_airline)

    async def delete_airline(
            self,
            session: AsyncSession,
            airline_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.airline_id == airline_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise AirlineNotFound(_id=airline_id)

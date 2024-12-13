from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, true
from sqlalchemy.exc import InterfaceError

from project.schemas.flight import FlightSchema, FlightCreateUpdateSchema
from project.infrastructure.postgres.models import Flight

from project.core.exceptions import FlightNotFound


class FlightRepository:
    _collection: Type[Flight] = Flight

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = select(true())

        try:
            return await session.scalar(query)
        except (Exception, InterfaceError):
            return False

    async def get_flight_by_id(
            self,
            session: AsyncSession,
            flight_id: int,
    ) -> FlightSchema:
        query = (
            select(self._collection)
            .where(self._collection.flight_id == flight_id)
        )

        flight = await session.scalar(query)

        if not flight:
            raise FlightNotFound(_id=flight_id)

        return FlightSchema.model_validate(obj=flight)

    async def get_all_flights(
            self,
            session: AsyncSession,
    ) -> list[FlightSchema]:
        query = select(self._collection)

        cities = await session.scalars(query)

        return [FlightSchema.model_validate(obj=flight) for flight in cities.all()]

    async def create_flight(
            self,
            session: AsyncSession,
            flight: FlightCreateUpdateSchema,
    ) -> FlightSchema:
        query = (
            insert(self._collection)
            .values(flight.model_dump())
            .returning(self._collection)
        )

        created_flight = await session.scalar(query)
        await session.flush()

        return FlightSchema.model_validate(obj=created_flight)

    async def update_flight(
            self,
            session: AsyncSession,
            flight_id: int,
            flight: FlightCreateUpdateSchema,
    ) -> FlightSchema:
        query = (
            update(self._collection)
            .where(self._collection.flight_id == flight_id)
            .values(flight.model_dump())
            .returning(self._collection)
        )

        updated_flight = await session.scalar(query)

        if not updated_flight:
            raise FlightNotFound(_id=flight_id)

        return FlightSchema.model_validate(obj=updated_flight)

    async def delete_flight(
            self,
            session: AsyncSession,
            flight_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.flight_id == flight_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise FlightNotFound(_id=flight_id)

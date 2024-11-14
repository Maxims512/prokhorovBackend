
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.schemas.flight import FlightSchema
from project.infrastructure.postgres.models import Flight

from project.core.config import settings


class FlightRepository:
    _collection: Type[Flight] = Flight

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def create_flight(
        self,
        session: AsyncSession,
        flight: FlightSchema,
    ) -> FlightSchema:
        columns = ", ".join(flight.model_dump().keys())
        values_placeholders = ", ".join(f":{key}" for key in flight.model_dump().keys())
        query = f"""
            INSERT INTO {settings.POSTGRES_SCHEMA}.flights ({columns})
            VALUES ({values_placeholders})
            RETURNING *;
        """

        result = await session.execute(text(query), flight.model_dump())
        await session.commit()

        new_flight = result.mappings().first()
        return FlightSchema.model_validate(obj=new_flight)

    async def get_flight_by_id(
        self,
        session: AsyncSession,
        id: int,
    ) -> FlightSchema:
        query = f"""
            SELECT * FROM {settings.POSTGRES_SCHEMA}.flights
            WHERE id = :id;
        """

        result = await session.execute(text(query), {'id': id})
        flight = result.mappings().first()

        return FlightSchema.model_validate(obj=flight) if flight else None

    async def update_flight(
        self,
        session: AsyncSession,
        id: int,
        flight: FlightSchema,
    ) -> FlightSchema:
        set_clause = ", ".join(f"{key} = :{key}" for key in flight.model_dump().keys())
        query = f"""
            UPDATE {settings.POSTGRES_SCHEMA}.flights
            SET {set_clause}
            WHERE id = :id
            RETURNING *;
        """

        params = flight.model_dump()
        params['id'] = id

        result = await session.execute(text(query), params)
        await session.commit()

        updated_flight = result.mappings().first()
        return FlightSchema.model_validate(obj=updated_flight) if updated_flight else None

    async def delete_flight(
        self,
        session: AsyncSession,
        id: int,
    ) -> dict:
        query = f"""
            DELETE FROM {settings.POSTGRES_SCHEMA}.flights
            WHERE id = :id;
        """

        await session.execute(text(query), {'id': id})
        await session.commit()

        return {'status': 'success', 'message': 'Flight deleted successfully'}

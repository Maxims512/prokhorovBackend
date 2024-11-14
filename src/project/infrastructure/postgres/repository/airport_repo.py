
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.schemas.airport import AirportSchema
from project.infrastructure.postgres.models import Airport

from project.core.config import settings


class AirportRepository:
    _collection: Type[Airport] = Airport

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def create_airport(
        self,
        session: AsyncSession,
        airport: AirportSchema,
    ) -> AirportSchema:
        columns = ", ".join(airport.model_dump().keys())
        values_placeholders = ", ".join(f":{key}" for key in airport.model_dump().keys())
        query = f"""
            INSERT INTO {settings.POSTGRES_SCHEMA}.airports ({columns})
            VALUES ({values_placeholders})
            RETURNING *;
        """

        result = await session.execute(text(query), airport.model_dump())
        await session.commit()

        new_airport = result.mappings().first()
        return AirportSchema.model_validate(obj=new_airport)

    async def get_airport_by_id(
        self,
        session: AsyncSession,
        id: int,
    ) -> AirportSchema:
        query = f"""
            SELECT * FROM {settings.POSTGRES_SCHEMA}.airports
            WHERE id = :id;
        """

        result = await session.execute(text(query), {'id': id})
        airport = result.mappings().first()

        return AirportSchema.model_validate(obj=airport) if airport else None

    async def update_airport(
        self,
        session: AsyncSession,
        id: int,
        airport: AirportSchema,
    ) -> AirportSchema:
        set_clause = ", ".join(f"{key} = :{key}" for key in airport.model_dump().keys())
        query = f"""
            UPDATE {settings.POSTGRES_SCHEMA}.airports
            SET {set_clause}
            WHERE id = :id
            RETURNING *;
        """

        params = airport.model_dump()
        params['id'] = id

        result = await session.execute(text(query), params)
        await session.commit()

        updated_airport = result.mappings().first()
        return AirportSchema.model_validate(obj=updated_airport) if updated_airport else None

    async def delete_airport(
        self,
        session: AsyncSession,
        id: int,
    ) -> dict:
        query = f"""
            DELETE FROM {settings.POSTGRES_SCHEMA}.airports
            WHERE id = :id;
        """

        await session.execute(text(query), {'id': id})
        await session.commit()

        return {'status': 'success', 'message': 'Airport deleted successfully'}

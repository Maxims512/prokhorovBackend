
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.schemas.airline import AirlineSchema
from project.infrastructure.postgres.models import Airline

from project.core.config import settings


class AirlineRepository:
    _collection: Type[Airline] = Airline

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False
    async def get_all_airlines(
        self,
        session: AsyncSession,
    ) -> list[AirlineSchema]:
        query = f"""
            SELECT * FROM {settings.POSTGRES_SCHEMA}.airlines;
        """

        result = await session.execute(text(query))
        airlines = result.mappings().all()

        return [AirlineSchema.model_validate(obj=airline) for airline in airlines]

    async def get_airline_by_id(
        self,
        session: AsyncSession,
        id: int,
    ) -> AirlineSchema:
        query = f"""
            SELECT * FROM {settings.POSTGRES_SCHEMA}.airlines
            WHERE id = :id;
        """

        result = await session.execute(text(query), {'id': id})
        airline = result.mappings().first()

        return AirlineSchema.model_validate(obj=airline) if airline else None

    async def insert_airline(
        self,
        session: AsyncSession,
        airline: AirlineSchema,
    ) -> AirlineSchema:
        columns = ", ".join(airline.model_dump().keys())
        values_placeholders = ", ".join(f":{key}" for key in airline.model_dump().keys())
        query = f"""
            INSERT INTO {settings.POSTGRES_SCHEMA}.airlines ({columns})
            VALUES ({values_placeholders})
            RETURNING *;
        """

        result = await session.execute(text(query), airline.model_dump())
        await session.commit()

        new_airline = result.mappings().first()
        return AirlineSchema.model_validate(obj=new_airline)

    async def update_airline(
        self,
        session: AsyncSession,
        id: int,
        airline: AirlineSchema,
    ) -> AirlineSchema:
        set_clause = ", ".join(f"{key} = :{key}" for key in airline.model_dump().keys())
        query = f"""
            UPDATE {settings.POSTGRES_SCHEMA}.airlines
            SET {set_clause}
            WHERE id = :id
            RETURNING *;
        """

        params = airline.model_dump()
        params['id'] = id

        result = await session.execute(text(query), params)
        await session.commit()

        updated_airline = result.mappings().first()
        return AirlineSchema.model_validate(obj=updated_airline) if updated_airline else None

    async def delete_airline(
        self,
        session: AsyncSession,
        id: int,
    ) -> dict:
        query = f"""
            DELETE FROM {settings.POSTGRES_SCHEMA}.airlines
            WHERE id = :id;
        """

        await session.execute(text(query), {'id': id})
        await session.commit()

        return {'status': 'success', 'message': 'Airline deleted successfully'}

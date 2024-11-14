
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.schemas.city import CitySchema
from project.infrastructure.postgres.models import City

from project.core.config import settings


class CityRepository:
    _collection: Type[City] = City

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_cities(
        self,
        session: AsyncSession,
    ) -> list[CitySchema]:
        query = f"""
            SELECT * FROM {settings.POSTGRES_SCHEMA}.cities;
        """

        result = await session.execute(text(query))
        cities = result.mappings().all()

        return [CitySchema.model_validate(obj=city) for city in cities]

    async def get_city_by_id(
        self,
        session: AsyncSession,
        id: int,
    ) -> CitySchema:
        query = f"""
            SELECT * FROM {settings.POSTGRES_SCHEMA}.cities
            WHERE id = :id;
        """

        result = await session.execute(text(query), {'id': id})
        city = result.mappings().first()

        return CitySchema.model_validate(obj=city) if city else None

    async def insert_city(
        self,
        session: AsyncSession,
        city: CitySchema,
    ) -> CitySchema:
        columns = ", ".join(city.model_dump().keys())
        values_placeholders = ", ".join(f":{key}" for key in city.model_dump().keys())
        query = f"""
            INSERT INTO {settings.POSTGRES_SCHEMA}.cities ({columns})
            VALUES ({values_placeholders})
            RETURNING *;
        """

        result = await session.execute(text(query), city.model_dump())
        await session.commit()

        new_city = result.mappings().first()
        return CitySchema.model_validate(obj=new_city)

    async def update_city(
        self,
        session: AsyncSession,
        id: int,
        city: CitySchema,
    ) -> CitySchema:
        set_clause = ", ".join(f"{key} = :{key}" for key in city.model_dump().keys())
        query = f"""
            UPDATE {settings.POSTGRES_SCHEMA}.cities
            SET {set_clause}
            WHERE id = :id
            RETURNING *;
        """

        params = city.model_dump()
        params['id'] = id

        result = await session.execute(text(query), params)
        await session.commit()

        updated_city = result.mappings().first()
        return CitySchema.model_validate(obj=updated_city) if updated_city else None

    async def delete_city(
        self,
        session: AsyncSession,
        id: int,
    ) -> dict:
        query = f"""
            DELETE FROM {settings.POSTGRES_SCHEMA}.cities
            WHERE id = :id;
        """

        await session.execute(text(query), {'id': id})
        await session.commit()

        return {'status': 'success', 'message': 'City deleted successfully'}

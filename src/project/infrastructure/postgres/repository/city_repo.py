from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, true
from sqlalchemy.exc import InterfaceError

from project.schemas.city import CitySchema, CityCreateUpdateSchema
from project.infrastructure.postgres.models import City

from project.core.exceptions import CityNotFound


class CityRepository:
    _collection: Type[City] = City

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = select(true())

        try:
            return await session.scalar(query)
        except (Exception, InterfaceError):
            return False

    async def get_city_by_id(
            self,
            session: AsyncSession,
            city_id: int,
    ) -> CitySchema:
        query = (
            select(self._collection)
            .where(self._collection.city_id == city_id)
        )

        city = await session.scalar(query)

        if not city:
            raise CityNotFound(_id=city_id)

        return CitySchema.model_validate(obj=city)

    async def get_all_cities(
            self,
            session: AsyncSession,
    ) -> list[CitySchema]:
        query = select(self._collection)

        cities = await session.scalars(query)

        return [CitySchema.model_validate(obj=city) for city in cities.all()]

    async def create_city(
            self,
            session: AsyncSession,
            city: CityCreateUpdateSchema,
    ) -> CitySchema:
        query = (
            insert(self._collection)
            .values(city.model_dump())
            .returning(self._collection)
        )

        created_city = await session.scalar(query)
        await session.flush()

        return CitySchema.model_validate(obj=created_city)

    async def update_city(
            self,
            session: AsyncSession,
            city_id: int,
            city: CityCreateUpdateSchema,
    ) -> CitySchema:
        query = (
            update(self._collection)
            .where(self._collection.city_id == city_id)
            .values(city.model_dump())
            .returning(self._collection)
        )

        updated_city = await session.scalar(query)

        if not updated_city:
            raise CityNotFound(_id=city_id)

        return CitySchema.model_validate(obj=updated_city)

    async def delete_city(
            self,
            session: AsyncSession,
            city_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.city_id == city_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise CityNotFound(_id=city_id)

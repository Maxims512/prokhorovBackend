from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, true
from sqlalchemy.exc import InterfaceError

from project.schemas.crew import CrewSchema, CrewCreateUpdateSchema
from project.infrastructure.postgres.models import Crew

from project.core.exceptions import CrewNotFound


class CrewRepository:
    _collection: Type[Crew] = Crew

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = select(true())

        try:
            return await session.scalar(query)
        except (Exception, InterfaceError):
            return False

    async def get_crew_by_id(
            self,
            session: AsyncSession,
            crew_id: int,
    ) -> CrewSchema:
        query = (
            select(self._collection)
            .where(self._collection.crew_id == crew_id)
        )

        crew = await session.scalar(query)

        if not crew:
            raise CrewNotFound(_id=crew_id)

        return CrewSchema.model_validate(obj=crew)

    async def get_all_crews(
            self,
            session: AsyncSession,
    ) -> list[CrewSchema]:
        query = select(self._collection)

        cities = await session.scalars(query)

        return [CrewSchema.model_validate(obj=crew) for crew in cities.all()]

    async def create_crew(
            self,
            session: AsyncSession,
            crew: CrewCreateUpdateSchema,
    ) -> CrewSchema:
        query = (
            insert(self._collection)
            .values(crew.model_dump())
            .returning(self._collection)
        )

        created_crew = await session.scalar(query)
        await session.flush()

        return CrewSchema.model_validate(obj=created_crew)

    async def update_crew(
            self,
            session: AsyncSession,
            crew_id: int,
            crew: CrewCreateUpdateSchema,
    ) -> CrewSchema:
        query = (
            update(self._collection)
            .where(self._collection.crew_id == crew_id)
            .values(crew.model_dump())
            .returning(self._collection)
        )

        updated_crew = await session.scalar(query)

        if not updated_crew:
            raise CrewNotFound(_id=crew_id)

        return CrewSchema.model_validate(obj=updated_crew)

    async def delete_crew(
            self,
            session: AsyncSession,
            crew_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.crew_id == crew_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise CrewNotFound(_id=crew_id)

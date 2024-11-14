
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.schemas.crew import CrewSchema
from project.infrastructure.postgres.models import Crew

from project.core.config import settings


class CrewRepository:
    _collection: Type[Crew] = Crew

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def create_crew(
        self,
        session: AsyncSession,
        crew: CrewSchema,
    ) -> CrewSchema:
        columns = ", ".join(crew.model_dump().keys())
        values_placeholders = ", ".join(f":{key}" for key in crew.model_dump().keys())
        query = f"""
            INSERT INTO {settings.POSTGRES_SCHEMA}.crew ({columns})
            VALUES ({values_placeholders})
            RETURNING *;
        """

        result = await session.execute(text(query), crew.model_dump())
        await session.commit()

        new_crew = result.mappings().first()
        return CrewSchema.model_validate(obj=new_crew)

    async def get_crew_by_id(
        self,
        session: AsyncSession,
        id: int,
    ) -> CrewSchema:
        query = f"""
            SELECT * FROM {settings.POSTGRES_SCHEMA}.crew
            WHERE id = :id;
        """

        result = await session.execute(text(query), {'id': id})
        crew = result.mappings().first()

        return CrewSchema.model_validate(obj=crew) if crew else None

    async def update_crew(
        self,
        session: AsyncSession,
        id: int,
        crew: CrewSchema,
    ) -> CrewSchema:
        set_clause = ", ".join(f"{key} = :{key}" for key in crew.model_dump().keys())
        query = f"""
            UPDATE {settings.POSTGRES_SCHEMA}.crew
            SET {set_clause}
            WHERE id = :id
            RETURNING *;
        """

        params = crew.model_dump()
        params['id'] = id

        result = await session.execute(text(query), params)
        await session.commit()

        updated_crew = result.mappings().first()
        return CrewSchema.model_validate(obj=updated_crew) if updated_crew else None

    async def delete_crew(
        self,
        session: AsyncSession,
        id: int,
    ) -> dict:
        query = f"""
            DELETE FROM {settings.POSTGRES_SCHEMA}.crew
            WHERE id = :id;
        """

        await session.execute(text(query), {'id': id})
        await session.commit()

        return {'status': 'success', 'message': 'Crew deleted successfully'}

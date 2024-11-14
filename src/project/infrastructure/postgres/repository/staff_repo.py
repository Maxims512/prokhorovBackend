
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.schemas.staff import StaffSchema
from project.infrastructure.postgres.models import Staff

from project.core.config import settings


class StaffRepository:
    _collection: Type[Staff] = Staff

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def create_staff(
        self,
        session: AsyncSession,
        staff: StaffSchema,
    ) -> StaffSchema:
        columns = ", ".join(staff.model_dump().keys())
        values_placeholders = ", ".join(f":{key}" for key in staff.model_dump().keys())
        query = f"""
            INSERT INTO {settings.POSTGRES_SCHEMA}.staff ({columns})
            VALUES ({values_placeholders})
            RETURNING *;
        """

        result = await session.execute(text(query), staff.model_dump())
        await session.commit()

        new_staff = result.mappings().first()
        return StaffSchema.model_validate(obj=new_staff)

    async def get_staff_by_id(
        self,
        session: AsyncSession,
        id: int,
    ) -> StaffSchema:
        query = f"""
            SELECT * FROM {settings.POSTGRES_SCHEMA}.staff
            WHERE id = :id;
        """

        result = await session.execute(text(query), {'id': id})
        staff = result.mappings().first()

        return StaffSchema.model_validate(obj=staff) if staff else None

    async def update_staff(
        self,
        session: AsyncSession,
        id: int,
        staff: StaffSchema,
    ) -> StaffSchema:
        set_clause = ", ".join(f"{key} = :{key}" for key in staff.model_dump().keys())
        query = f"""
            UPDATE {settings.POSTGRES_SCHEMA}.staff
            SET {set_clause}
            WHERE id = :id
            RETURNING *;
        """

        params = staff.model_dump()
        params['id'] = id

        result = await session.execute(text(query), params)
        await session.commit()

        updated_staff = result.mappings().first()
        return StaffSchema.model_validate(obj=updated_staff) if updated_staff else None

    async def delete_staff(
        self,
        session: AsyncSession,
        id: int,
    ) -> dict:
        query = f"""
            DELETE FROM {settings.POSTGRES_SCHEMA}.staff
            WHERE id = :id;
        """

        await session.execute(text(query), {'id': id})
        await session.commit()

        return {'status': 'success', 'message': 'Staff deleted successfully'}

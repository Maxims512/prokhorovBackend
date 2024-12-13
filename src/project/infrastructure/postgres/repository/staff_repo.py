from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, true
from sqlalchemy.exc import InterfaceError

from project.schemas.staff import StaffSchema, StaffCreateUpdateSchema
from project.infrastructure.postgres.models import Staff

from project.core.exceptions import StaffNotFound


class StaffRepository:
    _collection: Type[Staff] = Staff

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = select(true())

        try:
            return await session.scalar(query)
        except (Exception, InterfaceError):
            return False

    async def get_staff_by_id(
            self,
            session: AsyncSession,
            staff_id: int,
    ) -> StaffSchema:
        query = (
            select(self._collection)
            .where(self._collection.staff_id == staff_id)
        )

        staff = await session.scalar(query)

        if not staff:
            raise StaffNotFound(_id=staff_id)

        return StaffSchema.model_validate(obj=staff)

    async def get_all_staffs(
            self,
            session: AsyncSession,
    ) -> list[StaffSchema]:
        query = select(self._collection)

        cities = await session.scalars(query)

        return [StaffSchema.model_validate(obj=staff) for staff in cities.all()]

    async def create_staff(
            self,
            session: AsyncSession,
            staff: StaffCreateUpdateSchema,
    ) -> StaffSchema:
        query = (
            insert(self._collection)
            .values(staff.model_dump())
            .returning(self._collection)
        )

        created_staff = await session.scalar(query)
        await session.flush()

        return StaffSchema.model_validate(obj=created_staff)

    async def update_staff(
            self,
            session: AsyncSession,
            staff_id: int,
            staff: StaffCreateUpdateSchema,
    ) -> StaffSchema:
        query = (
            update(self._collection)
            .where(self._collection.staff_id == staff_id)
            .values(staff.model_dump())
            .returning(self._collection)
        )

        updated_staff = await session.scalar(query)

        if not updated_staff:
            raise StaffNotFound(_id=staff_id)

        return StaffSchema.model_validate(obj=updated_staff)

    async def delete_staff(
            self,
            session: AsyncSession,
            staff_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.staff_id == staff_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise StaffNotFound(_id=staff_id)

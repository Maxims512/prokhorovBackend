from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, true
from sqlalchemy.exc import InterfaceError

from project.schemas.discount import DiscountSchema, DiscountCreateUpdateSchema
from project.infrastructure.postgres.models import Discount

from project.core.exceptions import DiscountNotFound


class DiscountRepository:
    _collection: Type[Discount] = Discount

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = select(true())

        try:
            return await session.scalar(query)
        except (Exception, InterfaceError):
            return False

    async def get_discount_by_id(
            self,
            session: AsyncSession,
            discount_id: int,
    ) -> DiscountSchema:
        query = (
            select(self._collection)
            .where(self._collection.discount_id == discount_id)
        )

        discount = await session.scalar(query)

        if not discount:
            raise DiscountNotFound(_id=discount_id)

        return DiscountSchema.model_validate(obj=discount)

    async def get_all_discounts(
            self,
            session: AsyncSession,
    ) -> list[DiscountSchema]:
        query = select(self._collection)

        cities = await session.scalars(query)

        return [DiscountSchema.model_validate(obj=discount) for discount in cities.all()]

    async def create_discount(
            self,
            session: AsyncSession,
            discount: DiscountCreateUpdateSchema,
    ) -> DiscountSchema:
        query = (
            insert(self._collection)
            .values(discount.model_dump())
            .returning(self._collection)
        )

        created_discount = await session.scalar(query)
        await session.flush()

        return DiscountSchema.model_validate(obj=created_discount)

    async def update_discount(
            self,
            session: AsyncSession,
            discount_id: int,
            discount: DiscountCreateUpdateSchema,
    ) -> DiscountSchema:
        query = (
            update(self._collection)
            .where(self._collection.discount_id == discount_id)
            .values(discount.model_dump())
            .returning(self._collection)
        )

        updated_discount = await session.scalar(query)

        if not updated_discount:
            raise DiscountNotFound(_id=discount_id)

        return DiscountSchema.model_validate(obj=updated_discount)

    async def delete_discount(
            self,
            session: AsyncSession,
            discount_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.discount_id == discount_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise DiscountNotFound(_id=discount_id)

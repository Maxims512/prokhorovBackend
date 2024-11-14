
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.schemas.discount import DiscountSchema
from project.infrastructure.postgres.models import Discount

from project.core.config import settings


class DiscountRepository:
    _collection: Type[Discount] = Discount

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False


    async def create_discount(
        self,
        session: AsyncSession,
        discount: DiscountSchema,
    ) -> DiscountSchema:
        columns = ", ".join(discount.model_dump().keys())
        values_placeholders = ", ".join(f":{key}" for key in discount.model_dump().keys())
        query = f"""
            INSERT INTO {settings.POSTGRES_SCHEMA}.discounts ({columns})
            VALUES ({values_placeholders})
            RETURNING *;
        """

        result = await session.execute(text(query), discount.model_dump())
        await session.commit()

        new_discount = result.mappings().first()
        return DiscountSchema.model_validate(obj=new_discount)

    async def get_discount_by_id(
        self,
        session: AsyncSession,
        id: int,
    ) -> DiscountSchema:
        query = f"""
            SELECT * FROM {settings.POSTGRES_SCHEMA}.discounts
            WHERE id = :id;
        """

        result = await session.execute(text(query), {'id': id})
        discount = result.mappings().first()
        return DiscountSchema.model_validate(obj=discount) if discount else None

    async def update_discount(
        self,
        session: AsyncSession,
        id: int,
        discount: DiscountSchema,
    ) -> DiscountSchema:
        set_clause = ", ".join(f"{key} = :{key}" for key in discount.model_dump().keys())
        query = f"""
            UPDATE {settings.POSTGRES_SCHEMA}.discounts
            SET {set_clause}
            WHERE id = :id
            RETURNING *;
        """

        params = discount.model_dump()
        params['id'] = id

        result = await session.execute(text(query), params)
        await session.commit()

        updated_discount = result.mappings().first()
        return DiscountSchema.model_validate(obj=updated_discount) if updated_discount else None

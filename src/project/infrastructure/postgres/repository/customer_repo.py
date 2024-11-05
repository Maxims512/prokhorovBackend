from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.schemas.customer import CustomerSchema
from project.infrastructure.postgres.models import Customer

from project.core.config import settings


class CustomerRepository:
    _collection: Type[Customer] = Customer

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "SELECT 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_customers(
        self,
        session: AsyncSession,
    ) -> list[CustomerSchema]:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.customers;"

        result = await session.execute(text(query))

        customers = result.mappings().all()

        return [CustomerSchema.model_validate(obj=customer) for customer in customers]

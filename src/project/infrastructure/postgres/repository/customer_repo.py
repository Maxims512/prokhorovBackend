
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.schemas.customer import CustomerSchema
from project.infrastructure.postgres.models import Customer

from project.core.config import settings


class CustomerRepository:
    _collection: Type[Customer] = Customer

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_customers(
        self,
        session: AsyncSession,
    ) -> list[CustomerSchema]:
        query = f"""
            SELECT * FROM {settings.POSTGRES_SCHEMA}.customers;
        """

        result = await session.execute(text(query))
        customers = result.mappings().all()

        return [CustomerSchema.model_validate(obj=customer) for customer in customers]

    async def get_customer_by_id(
        self,
        session: AsyncSession,
        id: int,
    ) -> CustomerSchema:
        query = f"""
            SELECT * FROM {settings.POSTGRES_SCHEMA}.customers
            WHERE id = :id;
        """

        result = await session.execute(text(query), {'id': id})
        customer = result.mappings().first()

        return CustomerSchema.model_validate(obj=customer) if customer else None

    async def insert_customer(
        self,
        session: AsyncSession,
        customer: CustomerSchema,
    ) -> CustomerSchema:
        columns = ", ".join(customer.model_dump().keys())
        values_placeholders = ", ".join(f":{key}" for key in customer.model_dump().keys())
        query = f"""
            INSERT INTO {settings.POSTGRES_SCHEMA}.customers ({columns})
            VALUES ({values_placeholders})
            RETURNING *;
        """

        result = await session.execute(text(query), customer.model_dump())
        await session.commit()

        new_customer = result.mappings().first()
        return CustomerSchema.model_validate(obj=new_customer)

    async def update_customer(
        self,
        session: AsyncSession,
        id: int,
        customer: CustomerSchema,
    ) -> CustomerSchema:
        set_clause = ", ".join(f"{key} = :{key}" for key in customer.model_dump().keys())
        query = f"""
            UPDATE {settings.POSTGRES_SCHEMA}.customers
            SET {set_clause}
            WHERE id = :id
            RETURNING *;
        """

        params = customer.model_dump()
        params['id'] = id

        result = await session.execute(text(query), params)
        await session.commit()

        updated_customer = result.mappings().first()
        return CustomerSchema.model_validate(obj=updated_customer) if updated_customer else None

    async def delete_customer(
        self,
        session: AsyncSession,
        id: int,
    ) -> dict:
        query = f"""
            DELETE FROM {settings.POSTGRES_SCHEMA}.customers
            WHERE id = :id;
        """

        await session.execute(text(query), {'id': id})
        await session.commit()

        return {'status': 'success', 'message': 'Customer deleted successfully'}

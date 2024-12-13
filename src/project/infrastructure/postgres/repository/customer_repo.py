from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, true
from sqlalchemy.exc import IntegrityError, InterfaceError

from project.schemas.customer import CustomerSchema, CustomerCreateUpdateSchema

from project.infrastructure.postgres.models import Customer

from project.core.exceptions import CustomerNotFound, CustomerAlreadyExists


class CustomerRepository:
    _collection: Type[Customer] = Customer

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = select(true())

        try:
            return await session.scalar(query)
        except (Exception, InterfaceError):
            return False

    async def get_customer_by_email(
            self,
            session: AsyncSession,
            email: str,
    ) -> CustomerSchema:
        query = (
            select(self._collection)
            .where(self._collection.email == email)
        )

        customer = await session.scalar(query)

        if not customer:
            raise CustomerNotFound(_id=email)

        return CustomerSchema.model_validate(obj=customer)

    async def get_all_customers(
            self,
            session: AsyncSession,
    ) -> list[CustomerSchema]:
        query = select(self._collection)

        customers = await session.scalars(query)

        return [CustomerSchema.model_validate(obj=customer) for customer in customers.all()]

    async def get_customer_by_id(
            self,
            session: AsyncSession,
            customer_id: int,
    ) -> CustomerSchema:
        query = (
            select(self._collection)
            .where(self._collection.customer_id == customer_id)
        )

        customer = await session.scalar(query)

        if not customer:
            raise CustomerNotFound(_id=customer_id)

        return CustomerSchema.model_validate(obj=customer)

    async def create_customer(
            self,
            session: AsyncSession,
            customer: CustomerCreateUpdateSchema,
    ) -> CustomerSchema:
        query = (
            insert(self._collection)
            .values(customer.model_dump())
            .returning(self._collection)
        )

        try:
            created_customer = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise CustomerAlreadyExists(email=customer.email)

        return CustomerSchema.model_validate(obj=created_customer)

    async def update_customer(
            self,
            session: AsyncSession,
            customer_id: int,
            customer: CustomerCreateUpdateSchema,
    ) -> CustomerSchema:
        query = (
            update(self._collection)
            .where(self._collection.customer_id == customer_id)
            .values(customer.model_dump())
            .returning(self._collection)
        )

        updated_customer = await session.scalar(query)

        if not updated_customer:
            raise CustomerNotFound(_id=customer_id)

        return CustomerSchema.model_validate(obj=updated_customer)

    async def delete_customer(
            self,
            session: AsyncSession,
            customer_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.customer_id == customer_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise CustomerNotFound(_id=customer_id)

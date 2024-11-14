
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.schemas.ticket import TicketSchema
from project.infrastructure.postgres.models import Ticket

from project.core.config import settings


class TicketRepository:
    _collection: Type[Ticket] = Ticket

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def create_ticket(
        self,
        session: AsyncSession,
        ticket: TicketSchema,
    ) -> TicketSchema:
        columns = ", ".join(ticket.model_dump().keys())
        values_placeholders = ", ".join(f":{key}" for key in ticket.model_dump().keys())
        query = f"""
            INSERT INTO {settings.POSTGRES_SCHEMA}.tickets ({columns})
            VALUES ({values_placeholders})
            RETURNING *;
        """

        result = await session.execute(text(query), ticket.model_dump())
        await session.commit()

        new_ticket = result.mappings().first()
        return TicketSchema.model_validate(obj=new_ticket)

    async def get_ticket(
        self,
        session: AsyncSession,
        id: int,
    ) -> TicketSchema:
        query = f"""
            SELECT * FROM {settings.POSTGRES_SCHEMA}.tickets
            WHERE id = :id;
        """

        result = await session.execute(text(query), {'id': id})
        ticket = result.mappings().first()

        return TicketSchema.model_validate(obj=ticket) if ticket else None

    async def update_ticket(
        self,
        session: AsyncSession,
        id: int,
        ticket: TicketSchema,
    ) -> TicketSchema:
        set_clause = ", ".join(f"{key} = :{key}" for key in ticket.model_dump().keys())
        query = f"""
            UPDATE {settings.POSTGRES_SCHEMA}.tickets
            SET {set_clause}
            WHERE id = :id
            RETURNING *;
        """

        params = ticket.model_dump()
        params['id'] = id

        result = await session.execute(text(query), params)
        await session.commit()

        updated_ticket = result.mappings().first()
        return TicketSchema.model_validate(obj=updated_ticket) if updated_ticket else None

    async def delete_ticket(
        self,
        session: AsyncSession,
        id: int,
    ) -> bool:
        query = f"""
            DELETE FROM {settings.POSTGRES_SCHEMA}.tickets
            WHERE id = :id;
        """

        await session.execute(text(query), {'id': id})
        await session.commit()

        return True

from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, true
from sqlalchemy.exc import InterfaceError

from project.schemas.ticket import TicketSchema, TicketCreateUpdateSchema
from project.infrastructure.postgres.models import Ticket

from project.core.exceptions import TicketNotFound


class TicketRepository:
    _collection: Type[Ticket] = Ticket

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = select(true())

        try:
            return await session.scalar(query)
        except (Exception, InterfaceError):
            return False

    async def get_ticket_by_id(
            self,
            session: AsyncSession,
            ticket_id: int,
    ) -> TicketSchema:
        query = (
            select(self._collection)
            .where(self._collection.ticket_id == ticket_id)
        )

        ticket = await session.scalar(query)

        if not ticket:
            raise TicketNotFound(_id=ticket_id)

        return TicketSchema.model_validate(obj=ticket)

    async def get_all_tickets(
            self,
            session: AsyncSession,
    ) -> list[TicketSchema]:
        query = select(self._collection)

        cities = await session.scalars(query)

        return [TicketSchema.model_validate(obj=ticket) for ticket in cities.all()]

    async def create_ticket(
            self,
            session: AsyncSession,
            ticket: TicketCreateUpdateSchema,
    ) -> TicketSchema:
        query = (
            insert(self._collection)
            .values(ticket.model_dump())
            .returning(self._collection)
        )

        created_ticket = await session.scalar(query)
        await session.flush()

        return TicketSchema.model_validate(obj=created_ticket)

    async def update_ticket(
            self,
            session: AsyncSession,
            ticket_id: int,
            ticket: TicketCreateUpdateSchema,
    ) -> TicketSchema:
        query = (
            update(self._collection)
            .where(self._collection.ticket_id == ticket_id)
            .values(ticket.model_dump())
            .returning(self._collection)
        )

        updated_ticket = await session.scalar(query)

        if not updated_ticket:
            raise TicketNotFound(_id=ticket_id)

        return TicketSchema.model_validate(obj=updated_ticket)

    async def delete_ticket(
            self,
            session: AsyncSession,
            ticket_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.ticket_id == ticket_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise TicketNotFound(_id=ticket_id)

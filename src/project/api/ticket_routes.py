from fastapi import APIRouter, HTTPException, status

from project.infrastructure.postgres.database import PostgresDatabase
from project.infrastructure.postgres.repository.ticket_repo import TicketRepository
from project.schemas.ticket import TicketSchema, TicketCreateUpdateSchema

from project.core.exceptions import TicketNotFound

database = PostgresDatabase()
ticket_router = APIRouter()


@ticket_router.get(
    "/all_tickets",
    response_model=list[TicketSchema],
    status_code=status.HTTP_200_OK
)
async def get_all_users() -> list[TicketSchema]:
    async with database.session() as session:
        all_tickets = await TicketRepository().get_all_tickets(session=session)

    return all_tickets


@ticket_router.get(
    "/ticket/{ticket_id}",
    response_model=TicketSchema,
    status_code=status.HTTP_200_OK
)
async def get_ticket_by_id(
        ticket_id: int,
) -> TicketSchema:
    try:
        async with database.session() as session:
            ticket = await TicketRepository().get_ticket_by_id(session=session, ticket_id=ticket_id)
    except TicketNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return ticket


@ticket_router.post(
    "/add_ticket",
    response_model=TicketSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_ticket(
        ticket_dto: TicketCreateUpdateSchema,
) -> TicketSchema:
    async with database.session() as session:
        new_ticket = await TicketRepository().create_ticket(session=session, ticket=ticket_dto)

    return new_ticket


@ticket_router.put(
    "/update_ticket/{ticket_id}",
    response_model=TicketSchema,
    status_code=status.HTTP_200_OK,
)
async def update_ticket(
        ticket_id: int,
        ticket_dto: TicketCreateUpdateSchema,
) -> TicketSchema:
    try:
        async with database.session() as session:
            updated_ticket = await TicketRepository().update_ticket(
                session=session,
                ticket_id=ticket_id,
                ticket=ticket_dto,
            )
    except TicketNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_ticket


@ticket_router.delete(
    "/delete_ticket/{ticket_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_ticket(
        ticket_id: int,
) -> None:
    try:
        async with database.session() as session:
            ticket = await TicketRepository().delete_ticket(session=session, ticket_id=ticket_id)
    except TicketNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return ticket

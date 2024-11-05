from fastapi import APIRouter

from project.infrastructure.postgres.repository import customer_repo
from project.infrastructure.postgres.repository.customer_repo import CustomerRepository
from project.infrastructure.postgres.database import PostgresDatabase
from project.schemas.customer import CustomerSchema


router = APIRouter()



@router.get("/all_customers", response_model=list[CustomerSchema])
async def get_all_customers() -> list[CustomerSchema]:
    user_repo = CustomerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await customer_repo.check_connection(session=session)
        all_users = await customer_repo.get_all_customers(session=session)

    return all_users
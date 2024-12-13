from fastapi import APIRouter, HTTPException, status, Depends

from project.schemas.customer import CustomerSchema, CustomerCreateUpdateSchema

from project.core.exceptions import CustomerNotFound, CustomerAlreadyExists
from project.api.depends import database, customer_repo, get_current_customer, check_for_admin_access
from project.resource.auth import get_password_hash


customer_router = APIRouter()


@customer_router.get(
    "/all_customers",
    response_model=list[CustomerSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_customer)],
)
async def get_all_customers() -> list[CustomerSchema]:
    async with database.session() as session:
        all_customers = await customer_repo.get_all_customers(session=session)

    return all_customers


@customer_router.get(
    "/customer/{customer_id}",
    response_model=CustomerSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_customer)],
)
async def get_customer_by_id(
    customer_id: int,
) -> CustomerSchema:
    try:
        async with database.session() as session:
            customer = await customer_repo.get_Customer_by_id(session=session, Customer_id=customer_id)
    except CustomerNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return customer


@customer_router.post(
    "/add_customer",
    response_model=CustomerSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_customer(
    customer_dto: CustomerCreateUpdateSchema,
    current_customer: CustomerSchema = Depends(get_current_customer),
) -> CustomerSchema:
    check_for_admin_access(customer=current_customer)
    try:
        async with database.session() as session:
            customer_dto.password = get_password_hash(password=customer_dto.password)
            new_customer = await customer_repo.create_Customer(session=session, Customer=customer_dto)
    except CustomerAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_customer


@customer_router.put(
    "/update_customer/{customer_id}",
    response_model=CustomerSchema,
    status_code=status.HTTP_200_OK,
)
async def update_customer(
    customer_id: int,
    customer_dto: CustomerCreateUpdateSchema,
    current_customer: CustomerSchema = Depends(get_current_customer),
) -> CustomerSchema:
    check_for_admin_access(customer=current_customer)
    try:
        async with database.session() as session:
            customer_dto.password = get_password_hash(password=customer_dto.password)
            updated_customer = await customer_repo.update_customer(
                session=session,
                Customer_id=customer_id,
                Customer=customer_dto,
            )
    except CustomerNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_customer


@customer_router.delete(
    "/delete_customer/{customer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_customer(
    customer_id: int,
    current_customer: CustomerSchema = Depends(get_current_customer),
) -> None:
    check_for_admin_access(customer=current_customer)
    try:
        async with database.session() as session:
            customer = await customer_repo.delete_Customer(session=session, customer_id=customer_id)
    except CustomerNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return customer

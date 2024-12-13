from fastapi import APIRouter, HTTPException, status

from project.infrastructure.postgres.database import PostgresDatabase
from project.infrastructure.postgres.repository.staff_repo import StaffRepository
from project.schemas.staff import StaffSchema, StaffCreateUpdateSchema

from project.core.exceptions import StaffNotFound

database = PostgresDatabase()
staff_router = APIRouter()


@staff_router.get(
    "/all_staffs",
    response_model=list[StaffSchema],
    status_code=status.HTTP_200_OK
)
async def get_all_users() -> list[StaffSchema]:
    async with database.session() as session:
        all_staffs = await StaffRepository().get_all_staffs(session=session)

    return all_staffs


@staff_router.get(
    "/staff/{staff_id}",
    response_model=StaffSchema,
    status_code=status.HTTP_200_OK
)
async def get_staff_by_id(
        staff_id: int,
) -> StaffSchema:
    try:
        async with database.session() as session:
            staff = await StaffRepository().get_staff_by_id(session=session, staff_id=staff_id)
    except StaffNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return staff


@staff_router.post(
    "/add_staff",
    response_model=StaffSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_staff(
        staff_dto: StaffCreateUpdateSchema,
) -> StaffSchema:
    async with database.session() as session:
        new_staff = await StaffRepository().create_staff(session=session, staff=staff_dto)

    return new_staff


@staff_router.put(
    "/update_staff/{staff_id}",
    response_model=StaffSchema,
    status_code=status.HTTP_200_OK,
)
async def update_staff(
        staff_id: int,
        staff_dto: StaffCreateUpdateSchema,
) -> StaffSchema:
    try:
        async with database.session() as session:
            updated_staff = await StaffRepository().update_staff(
                session=session,
                staff_id=staff_id,
                staff=staff_dto,
            )
    except StaffNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_staff


@staff_router.delete(
    "/delete_staff/{staff_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_staff(
        staff_id: int,
) -> None:
    try:
        async with database.session() as session:
            staff = await StaffRepository().delete_staff(session=session, staff_id=staff_id)
    except StaffNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return staff

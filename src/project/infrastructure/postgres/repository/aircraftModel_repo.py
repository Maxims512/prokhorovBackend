from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, true
from sqlalchemy.exc import InterfaceError

from project.schemas.aircraftModel import AircraftModelSchema, AircraftModelCreateUpdateSchema
from project.infrastructure.postgres.models import AircraftModel

from project.core.exceptions import AircraftModelNotFound


class AircraftModelRepository:
    _collection: Type[AircraftModel] = AircraftModel

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = select(true())

        try:
            return await session.scalar(query)
        except (Exception, InterfaceError):
            return False

    async def get_aircraft_model_by_id(
            self,
            session: AsyncSession,
            aircraft_model_id: int,
    ) -> AircraftModelSchema:
        query = (
            select(self._collection)
            .where(self._collection.aircraft_model_id == aircraft_model_id)
        )

        aircraft_model = await session.scalar(query)

        if not aircraft_model:
            raise AircraftModelNotFound(_id=aircraft_model_id)

        return AircraftModelSchema.model_validate(obj=aircraft_model)

    async def get_all_aircraft_models(
            self,
            session: AsyncSession,
    ) -> list[AircraftModelSchema]:
        query = select(self._collection)

        aircraft_models = await session.scalars(query)

        return [AircraftModelSchema.model_validate(obj=aircraft_model) for aircraft_model in aircraft_models.all()]

    async def create_aircraft_model(
            self,
            session: AsyncSession,
            aircraft_model: AircraftModelCreateUpdateSchema,
    ) -> AircraftModelSchema:
        query = (
            insert(self._collection)
            .values(aircraft_model.model_dump())
            .returning(self._collection)
        )

        created_aircraft_model = await session.scalar(query)
        await session.flush()

        return AircraftModelSchema.model_validate(obj=created_aircraft_model)

    async def update_aircraft_model(
            self,
            session: AsyncSession,
            aircraft_model_id: int,
            aircraft_model: AircraftModelCreateUpdateSchema,
    ) -> AircraftModelSchema:
        query = (
            update(self._collection)
            .where(self._collection.aircraft_model_id == aircraft_model_id)
            .values(aircraft_model.model_dump())
            .returning(self._collection)
        )

        updated_aircraft_model = await session.scalar(query)

        if not updated_aircraft_model:
            raise AircraftModelNotFound(_id=aircraft_model_id)

        return AircraftModelSchema.model_validate(obj=updated_aircraft_model)

    async def delete_aircraft_model(
            self,
            session: AsyncSession,
            aircraft_model_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.aircraft_model_id == aircraft_model_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise AircraftModelNotFound(_id=aircraft_model_id)



from sqlalchemy.orm import Mapped, mapped_column

from project.infrastructure.postgres.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[str] = mapped_column(nullable=False)
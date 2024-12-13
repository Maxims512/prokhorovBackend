from datetime import datetime

from sqlalchemy import (
    String, ForeignKey, false
)
from sqlalchemy.orm import relationship, Mapped, mapped_column


from project.infrastructure.postgres.database import Base




class City(Base):
    __tablename__ = "cities"

    city_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    country: Mapped[str] = mapped_column(String)

    airports: Mapped[list["Airport"]] = relationship("Airport", back_populates="city")


class AircraftModel(Base):
    __tablename__ = "AircraftModel"

    aircraft_model_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    capacity: Mapped[int] = mapped_column()
    max_range: Mapped[int] = mapped_column()

    planes: Mapped[list["Plane"]] = relationship("Plane", back_populates="aircraft_model")


class Airline(Base):
    __tablename__ = "Airline"

    airline_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    rating: Mapped[float] = mapped_column()

    planes: Mapped[list["Plane"]] = relationship("Plane", back_populates="airline")
    staff: Mapped[list["Staff"]] = relationship("Staff", back_populates="airline")
    flights: Mapped[list["Flight"]] = relationship("Flight", back_populates="airline")


class Customer(Base):
    __tablename__ = "Customers"

    customer_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String)
    second_name: Mapped[str] = mapped_column(String)
    age: Mapped[int] = mapped_column()
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=false())

    discounts: Mapped[list["Discount"]] = relationship("Discount", back_populates="customer")
    tickets: Mapped[list["Ticket"]] = relationship("Ticket", back_populates="customer")


class Plane(Base):
    __tablename__ = "Plane"

    plane_id: Mapped[int] = mapped_column(primary_key=True)
    airline_id: Mapped[int] = mapped_column(ForeignKey("Airline.airline_id"))
    year_of_release: Mapped[int] = mapped_column()
    aircraft_model_id: Mapped[int] = mapped_column(ForeignKey("AircraftModel.aircraft_model_id"))

    airline: Mapped["Airline"] = relationship("Airline", back_populates="planes")
    aircraft_model: Mapped["AircraftModel"] = relationship("AircraftModel", back_populates="planes")
    flights: Mapped[list["Flight"]] = relationship("Flight", back_populates="plane")


class Discount(Base):
    __tablename__ = "Discount"

    discount_id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("Customers.customer_id"))
    discount_percent: Mapped[int] = mapped_column()

    customer: Mapped["Customer"] = relationship("Customer", back_populates="discounts")


class Airport(Base):
    __tablename__ = "Airport"

    airport_id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.city_id"))
    airport_code: Mapped[str] = mapped_column(String)

    city: Mapped["City"] = relationship("City", back_populates="airports")
    routes: Mapped[list["Route"]] = relationship("Route", back_populates="departure_airport")
    arrival_routes: Mapped[list["Route"]] = relationship("Route", back_populates="arrival_airport")


class Staff(Base):
    __tablename__ = "Staff"

    staff_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String)
    second_name: Mapped[str] = mapped_column(String)
    airline_id: Mapped[int] = mapped_column(ForeignKey("Airline.airline_id"))
    experience: Mapped[int] = mapped_column()

    airline: Mapped["Airline"] = relationship("Airline", back_populates="staff")
    crew: Mapped[list["Crew"]] = relationship("Crew", back_populates="pilot1_id")


class Crew(Base):
    __tablename__ = "Crew"

    crew_id: Mapped[int] = mapped_column(primary_key=True)
    pilot1_id: Mapped[int] = mapped_column(ForeignKey("Staff.employee_id"))
    pilot2_id: Mapped[int] = mapped_column(ForeignKey("Staff.employee_id"))
    stewardess: Mapped[int] = mapped_column(ForeignKey("Staff.employee_id"))
    flights: Mapped[list["Flight"]] = relationship("Flight", back_populates="crew")


class Route(Base):
    __tablename__ = "Routes"

    route_id: Mapped[int] = mapped_column(primary_key=True)
    departure_airport_id: Mapped[int] = mapped_column(ForeignKey("Airport.airport_id"))
    arrival_airport_id: Mapped[int] = mapped_column(ForeignKey("Airport.airport_id"))
    distance: Mapped[float] = mapped_column()

    departure_airport: Mapped["Airport"] = relationship("Airport", foreign_keys=[departure_airport_id],
                                                        back_populates="routes")
    arrival_airport: Mapped["Airport"] = relationship("Airport", foreign_keys=[arrival_airport_id],
                                                      back_populates="arrival_routes")
    flights: Mapped[list["Flight"]] = relationship("Flight", back_populates="route")


class Flight(Base):
    __tablename__ = "Flights"

    flight_id: Mapped[int] = mapped_column(primary_key=True)
    route_id: Mapped[int] = mapped_column(ForeignKey("Routes.route_id"))
    plane_id: Mapped[int] = mapped_column(ForeignKey("Plane.plane_id"))
    crew_id: Mapped[int] = mapped_column(ForeignKey("Crew.crew_id"))
    airline_id: Mapped[int] = mapped_column(ForeignKey("Airline.airline_id"))
    departure_time: Mapped[datetime] = mapped_column()
    arrival_time: Mapped[datetime] = mapped_column()

    route: Mapped["Route"] = relationship("Route", back_populates="flights")
    plane: Mapped["Plane"] = relationship("Plane", back_populates="flights")
    crew: Mapped["Crew"] = relationship("Crew", back_populates="flights")
    airline: Mapped["Airline"] = relationship("Airline", back_populates="flights")


class Ticket(Base):
    __tablename__ = "Tickets"

    ticket_id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("Customers.customer_id"))
    date_of_purchase: Mapped[datetime] = mapped_column()
    price: Mapped[float] = mapped_column()
    flight_id: Mapped[int] = mapped_column(ForeignKey("Flights.flight_id"))

    customer: Mapped["Customer"] = relationship("Customer", back_populates="tickets")
    flight: Mapped["Flight"] = relationship("Flight", back_populates="tickets")

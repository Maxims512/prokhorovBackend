from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, Float, DateTime, Time
from src.project.infrastructure.postgres.database import Base

class City(Base):
    tablename = "cities"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)

    airports = relationship("Airport", back_populates="city")


class AircraftModel(Base):
    tablename = "AircraftModel"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    capacity: Mapped[int] = mapped_column(nullable=False)
    max_range: Mapped[int] = mapped_column(nullable=False)

    planes = relationship("Plane", back_populates="aircraft_model")



class Airline(Base):
    tablename = "Airline"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    rating: Mapped[float] = mapped_column(nullable=False)

    planes = relationship("Plane", back_populates="airline")
    staff = relationship("Staff", back_populates="airline")
    flights = relationship("Flight", back_populates="airline")


class Customer(Base):
    tablename = "Customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    second_name: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)

    discounts = relationship("Discount", back_populates="customer")
    tickets = relationship("Ticket", back_populates="customer")



class Plane(Base):
    tablename = "Plane"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_airline: Mapped[int] = mapped_column(ForeignKey("Airline.id"), nullable=False)
    year_of_release: Mapped[int] = mapped_column(nullable=False)
    id_aircraft_model: Mapped[int] = mapped_column(ForeignKey("AircraftModel.id"), nullable=False)

    airline = relationship("Airline", back_populates="planes")
    aircraft_model = relationship("AircraftModel", back_populates="planes")
    flights = relationship("Flight", back_populates="plane")


class Discount(Base):
    tablename = "Discount"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_customer: Mapped[int] = mapped_column(ForeignKey("Customers.id"), nullable=False)
    discount_percent: Mapped[int] = mapped_column(nullable=False)

    customer = relationship("Customer", back_populates="discounts")


class Airport(Base):
    tablename = "Airport"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_city: Mapped[int] = mapped_column(ForeignKey("cities.id"), nullable=False)
    airport_code: Mapped[str] = mapped_column(nullable=False)

    city = relationship("City", back_populates="airports")

    departures = relationship(
        "Route",
        back_populates="departure_airport",
        foreign_keys="Route.id_departure_airport"
    )
    arrivals = relationship(
        "Route",
        back_populates="arrival_airport",
        foreign_keys="Route.id_arrival_airport"
    )

class Staff(Base):
    tablename = "Staff"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    second_name: Mapped[str] = mapped_column(nullable=False)
    id_airline: Mapped[int] = mapped_column(ForeignKey("Airline.id"), nullable=False)
    experience: Mapped[int] = mapped_column(nullable=False)

    airline = relationship("Airline", back_populates="staff")

    crews_as_pilot1 = relationship(
        "Crew",
        back_populates="pilot1",
        foreign_keys="Crew.id_pilot1"
    )
    crews_as_pilot2 = relationship(
        "Crew",
        back_populates="pilot2",
        foreign_keys="Crew.id_pilot2"
    )
    crews_as_stewardess = relationship(
        "Crew",
        back_populates="stewardess",
        foreign_keys="Crew.id_stewardess"
    )


class Crew(Base):
    tablename = "Crew"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_pilot1: Mapped[int] = mapped_column(ForeignKey("Staff.id"), nullable=False)
    id_pilot2: Mapped[int] = mapped_column(ForeignKey("Staff.id"), nullable=False)
    id_stewardess: Mapped[int] = mapped_column(ForeignKey("Staff.id"), nullable=False)

    pilot1 = relationship(
        "Staff",
        back_populates="crews_as_pilot1",
        foreign_keys=[id_pilot1]
    )
    pilot2 = relationship(
        "Staff",
        back_populates="crews_as_pilot2",
        foreign_keys=[id_pilot2]
    )
    stewardess = relationship(
        "Staff",
        back_populates="crews_as_stewardess",
        foreign_keys=[id_stewardess]
    )

    flights = relationship("Flight", back_populates="crew")


class Route(Base):
    tablename = "Routes"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_departure_airport: Mapped[int] = mapped_column(ForeignKey("Airport.id"), nullable=False)
    id_arrival_airport: Mapped[int] = mapped_column(ForeignKey("Airport.id"), nullable=False)
    distance: Mapped[float] = mapped_column(nullable=False)
    flight_time: Mapped[Time] = mapped_column(nullable=False)

    departure_airport = relationship(
        "Airport",
        back_populates="departures",
        foreign_keys=[id_departure_airport]
    )
    arrival_airport = relationship(
        "Airport",
        back_populates="arrivals",
        foreign_keys=[id_arrival_airport]
    )

    flights = relationship("Flight", back_populates="route")

class Flight(Base):
    tablename = "Flights"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_route: Mapped[int] = mapped_column(ForeignKey("Routes.id"), nullable=False)
    id_plane: Mapped[int] = mapped_column(ForeignKey("Plane.id"), nullable=False)
    id_crew: Mapped[int] = mapped_column(ForeignKey("Crew.id"), nullable=False)
    id_airline: Mapped[int] = mapped_column(ForeignKey("Airline.id"), nullable=False)
    departure_time: Mapped[DateTime] = mapped_column(nullable=False)
    arrival_time: Mapped[DateTime] = mapped_column(nullable=False)

    route = relationship("Route", back_populates="flights")
    plane = relationship("Plane", back_populates="flights")
    crew = relationship("Crew", back_populates="flights")
    airline = relationship("Airline", back_populates="flights")

    tickets = relationship("Ticket", back_populates="flight")

class Ticket(Base):
    tablename = "Tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_customer: Mapped[int] = mapped_column(ForeignKey("Customers.id"), nullable=False)
    date_of_purchase: Mapped[DateTime] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    id_flight: Mapped[int] = mapped_column(ForeignKey("Flights.id"), nullable=False)

    customer = relationship("Customer", back_populates="tickets")
    flight = relationship("Flight", back_populates="tickets")

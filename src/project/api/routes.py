from http.client import HTTPException

from fastapi import APIRouter

from project.infrastructure.postgres.repository.city_repo import CityRepository
from project.schemas.city import CitySchema

from project.infrastructure.postgres.repository.aircraft_model_repo import AircraftModelRepository
from project.schemas.aircraftModel import AircraftModelSchema

from project.infrastructure.postgres.repository.airline_repo import AirlineRepository
from project.schemas.airline import AirlineSchema

from project.infrastructure.postgres.repository.customer_repo import CustomerRepository
from project.schemas.customer import CustomerSchema

from project.infrastructure.postgres.repository.plane_repo import PlaneRepository
from project.schemas.plane import PlaneSchema

from project.infrastructure.postgres.repository.discount_repo import DiscountRepository
from project.schemas.discount import DiscountSchema

from project.infrastructure.postgres.repository.airport_repo import AirportRepository
from project.schemas.airport import AirportSchema

from project.infrastructure.postgres.repository.staff_repo import StaffRepository
from project.schemas.staff import StaffSchema

from project.infrastructure.postgres.repository.crew_repo import CrewRepository
from project.schemas.crew import CrewSchema

from project.infrastructure.postgres.repository.route_repo import RouteRepository
from project.schemas.route import RouteSchema

from project.infrastructure.postgres.repository.flight_repo import FlightRepository
from project.schemas.flight import FlightSchema

from project.infrastructure.postgres.repository.ticket_repo import TicketRepository
from project.schemas.ticket import TicketSchema


from project.infrastructure.postgres.database import PostgresDatabase

from project.schemas.city import CitySchema
from project.schemas.aircraftModel import AircraftModelSchema

router = APIRouter()


@router.get("/all_cities", response_model=list[CitySchema])
async def get_all_cities() -> list[CitySchema]:
    city_repo = CityRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await city_repo.check_connection(session=session)
        all_cities = await city_repo.get_all_cities(session=session)

    return all_cities

@router.get("/city/{id}", response_model=CitySchema)
async def get_city_by_id(id: int) -> CitySchema:
    city_repo = CityRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await city_repo.check_connection(session=session)
        city = await city_repo.get_city_by_id(session=session, city_id=id)

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    return city


@router.post("/city", response_model=CitySchema)
async def insert_city(city: CitySchema) -> CitySchema:
    city_repo = CityRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await city_repo.check_connection(session=session)
        new_city = await city_repo.insert_city(
            session=session,
            title=city.title,
            country=city.country
        )

    if not new_city:
        raise HTTPException(status_code=500, detail="Failed to insert city")

    return new_city


@router.put("/city/{id}", response_model=CitySchema)
async def update_city(id: int, city: CitySchema) -> CitySchema:
    city_repo = CityRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await city_repo.check_connection(session=session)
        updated_city = await city_repo.update_city(
            session=session,
            city_id=id,
            title=city.title,
            country=city.country
        )

    if not updated_city:
        raise HTTPException(status_code=404, detail="City not found or failed to update")

    return updated_city

@router.delete("/city/{id}", response_model=dict)
async def delete_city(id: int) -> dict:
    city_repo = CityRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await city_repo.check_connection(session=session)
        deleted = await city_repo.delete_city_by_id(session=session, city_id=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="City not found or failed to delete")

    return {"message": "City deleted successfully"}

######################################3

@router.get("/all_aircraft_models", response_model=list[AircraftModelSchema])
async def get_all_aircraft_models() -> list[AircraftModelSchema]:
    aircraft_model_repo = AircraftModelRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await aircraft_model_repo.check_connection(session=session)
        all_aircraft_models = await aircraft_model_repo.get_all_aircraft_models(session=session)

    return all_aircraft_models


@router.get("/aircraft_model/{id}", response_model=AircraftModelSchema)
async def get_aircraft_model_by_id(id: int) -> AircraftModelSchema:
    aircraft_model_repo = AircraftModelRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await aircraft_model_repo.check_connection(session=session)
        aircraft_model = await aircraft_model_repo.get_aircraft_model_by_id(session=session, aircraft_model_id=id)

    if not aircraft_model:
        raise HTTPException(status_code=404, detail="Aircraft model not found")

    return aircraft_model

@router.post("/aircraft_model", response_model=AircraftModelSchema)
async def insert_aircraft_model(aircraft_model: AircraftModelSchema) -> AircraftModelSchema:
    aircraft_model_repo = AircraftModelRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await aircraft_model_repo.check_connection(session=session)
        new_aircraft_model = await aircraft_model_repo.insert_aircraft_model(
            session=session,
            title=aircraft_model.title,
            capacity=aircraft_model.capacity,
            max_range=aircraft_model.max_range
        )

    if not new_aircraft_model:
        raise HTTPException(status_code=500, detail="Failed to insert aircraft model")

    return new_aircraft_model



@router.put("/aircraft_model/{id}", response_model=AircraftModelSchema)
async def update_aircraft_model(id: int, aircraft_model: AircraftModelSchema) -> AircraftModelSchema:
    aircraft_model_repo = AircraftModelRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await aircraft_model_repo.check_connection(session=session)
        updated_aircraft_model = await aircraft_model_repo.update_aircraft_model(
            session=session,
            aircraft_model_id=id,
            title=aircraft_model.title,
            capacity=aircraft_model.capacity,
            max_range=aircraft_model.max_range
        )

    if not updated_aircraft_model:
        raise HTTPException(status_code=404, detail="Aircraft model not found or failed to update")

    return updated_aircraft_model

@router.delete("/aircraft_model/{id}", response_model=dict)
async def delete_aircraft_model(id: int) -> dict:
    aircraft_model_repo = AircraftModelRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await aircraft_model_repo.check_connection(session=session)
        deleted = await aircraft_model_repo.delete_aircraft_model_by_id(session=session, aircraft_model_id=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Aircraft model not found or failed to delete")

    return {"message": "Aircraft model deleted successfully"}



@router.get("/all_airlines", response_model=list[AirlineSchema])
async def get_all_airlines() -> list[AirlineSchema]:
    airline_repo = AirlineRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await airline_repo.check_connection(session=session)
        all_airlines = await airline_repo.get_all_airlines(session=session)

    return all_airlines


@router.get("/airline/{id}", response_model=AirlineSchema)
async def get_airline_by_id(id: int) -> AirlineSchema:
    airline_repo = AirlineRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await airline_repo.check_connection(session=session)
        airline = await airline_repo.get_airline_by_id(session=session, airline_id=id)

    if not airline:
        raise HTTPException(status_code=404, detail="Airline not found")

    return airline



@router.post("/airline", response_model=AirlineSchema)
async def insert_airline(airline: AirlineSchema) -> AirlineSchema:
    airline_repo = AirlineRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await airline_repo.check_connection(session=session)
        new_airline = await airline_repo.insert_airline(
            session=session,
            title=airline.title,
            rating=airline.rating
        )

    if not new_airline:
        raise HTTPException(status_code=500, detail="Failed to insert airline")

    return new_airline


@router.put("/airline/{id}", response_model=AirlineSchema)
async def update_airline(id: int, airline: AirlineSchema) -> AirlineSchema:
    airline_repo = AirlineRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await airline_repo.check_connection(session=session)
        updated_airline = await airline_repo.update_airline(
            session=session,
            airline_id=id,
            title=airline.title,
            rating=airline.rating
        )

    if not updated_airline:
        raise HTTPException(status_code=404, detail="Airline not found or failed to update")

    return updated_airline



@router.delete("/airline/{id}", response_model=dict)
async def delete_airline(id: int) -> dict:
    airline_repo = AirlineRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await airline_repo.check_connection(session=session)
        deleted = await airline_repo.delete_airline_by_id(session=session, airline_id=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Airline not found or failed to delete")

    return {"message": "Airline deleted successfully"}



@router.get("/all_customers", response_model=list[CustomerSchema])
async def get_all_customers() -> list[CustomerSchema]:
    customer_repo = CustomerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await customer_repo.check_connection(session=session)
        all_customers = await customer_repo.get_all_customers(session=session)

    return all_customers



@router.get("/customer/{id}", response_model=CustomerSchema)
async def get_customer_by_id(id: int) -> CustomerSchema:
    customer_repo = CustomerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await customer_repo.check_connection(session=session)
        customer = await customer_repo.get_customer_by_id(session=session, customer_id=id)

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return customer



@router.post("/customer", response_model=CustomerSchema)
async def insert_customer(customer: CustomerSchema) -> CustomerSchema:
    customer_repo = CustomerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await customer_repo.check_connection(session=session)
        new_customer = await customer_repo.insert_customer(
            session=session,
            first_name=customer.first_name,
            second_name=customer.second_name,
            age=customer.age
        )

    if not new_customer:
        raise HTTPException(status_code=500, detail="Failed to insert customer")

    return new_customer


@router.put("/customer/{id}", response_model=CustomerSchema)
async def update_customer(id: int, customer: CustomerSchema) -> CustomerSchema:
    customer_repo = CustomerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await customer_repo.check_connection(session=session)
        updated_customer = await customer_repo.update_customer(
            session=session,
            customer_id=id,
            first_name=customer.first_name,
            second_name=customer.second_name,
            age=customer.age
        )

    if not updated_customer:
        raise HTTPException(status_code=404, detail="Customer not found or failed to update")

    return updated_customer


@router.delete("/customer/{id}", response_model=dict)
async def delete_customer(id: int) -> dict:
    customer_repo = CustomerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await customer_repo.check_connection(session=session)
        deleted = await customer_repo.delete_customer_by_id(session=session, customer_id=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Customer not found or failed to delete")

    return {"message": "Customer deleted successfully"}



@router.post("/plane", response_model=PlaneSchema)
async def create_plane(plane: PlaneSchema) -> PlaneSchema:
    plane_repo = PlaneRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await plane_repo.check_connection(session=session)
        new_plane = await plane_repo.create_plane(
            session=session,
            airline_id=plane.airline_id,
            year_of_release=plane.year_of_release,
            aircraft_model_id=plane.aircraft_model_id
        )

    return new_plane


@router.get("/plane/{id}", response_model=PlaneSchema)
async def get_plane(id: int) -> PlaneSchema:
    plane_repo = PlaneRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await plane_repo.check_connection(session=session)
        plane = await plane_repo.get_plane(session=session, plane_id=id)

    if not plane:
        raise HTTPException(status_code=404, detail="Plane not found")

    return plane


@router.put("/plane/{id}", response_model=PlaneSchema)
async def update_plane(id: int, plane: PlaneSchema) -> PlaneSchema:
    plane_repo = PlaneRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await plane_repo.check_connection(session=session)
        updated_plane = await plane_repo.update_plane(
            session=session,
            plane_id=id,
            airline_id=plane.airline_id,
            year_of_release=plane.year_of_release,
            aircraft_model_id=plane.aircraft_model_id
        )

    if not updated_plane:
        raise HTTPException(status_code=404, detail="Plane not found or failed to update")

    return updated_plane


@router.delete("/plane/{id}")
async def delete_plane(id: int):
    plane_repo = PlaneRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await plane_repo.check_connection(session=session)
        deleted_plane = await plane_repo.delete_plane(session=session, plane_id=id)

    if not deleted_plane:
        raise HTTPException(status_code=404, detail="Plane not found or failed to delete")

    return {"message": "Plane deleted successfully"}


@router.post("/discount", response_model=DiscountSchema)
async def create_discount(discount: DiscountSchema) -> DiscountSchema:
    discount_repo = DiscountRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await discount_repo.check_connection(session=session)
        new_discount = await discount_repo.create_discount(
            session=session,
            customer_id=discount.customer_id,
            discount_percent=discount.discount_percent
        )

    return new_discount


@router.get("/discount/{id}", response_model=DiscountSchema)
async def get_discount(id: int) -> DiscountSchema:
    discount_repo = DiscountRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await discount_repo.check_connection(session=session)
        discount = await discount_repo.get_discount(session=session, discount_id=id)

    if not discount:
        raise HTTPException(status_code=404, detail="Discount not found")

    return discount


@router.put("/discount/{id}", response_model=DiscountSchema)
async def update_discount(id: int, discount: DiscountSchema) -> DiscountSchema:
    discount_repo = DiscountRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await discount_repo.check_connection(session=session)
        updated_discount = await discount_repo.update_discount(
            session=session,
            discount_id=id,
            customer_id=discount.customer_id,
            discount_percent=discount.discount_percent
        )

    if not updated_discount:
        raise


@router.post("/airport", response_model=AirportSchema)
async def create_airport(airport: AirportSchema) -> AirportSchema:
    airport_repo = AirportRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await airport_repo.check_connection(session=session)
        new_airport = await airport_repo.create_airport(
            session=session,
            city_id=airport.city_id,
            airport_code=airport.airport_code
        )

    return new_airport


@router.get("/airport/{id}", response_model=AirportSchema)
async def get_airport(id: int) -> AirportSchema:
    airport_repo = AirportRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await airport_repo.check_connection(session=session)
        airport = await airport_repo.get_airport(session=session, airport_id=id)

    if not airport:
        raise HTTPException(status_code=404, detail="Airport not found")

    return airport


@router.put("/airport/{id}", response_model=AirportSchema)
async def update_airport(id: int, airport: AirportSchema) -> AirportSchema:
    airport_repo = AirportRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await airport_repo.check_connection(session=session)
        updated_airport = await airport_repo.update_airport(
            session=session,
            airport_id=id,
            city_id=airport.city_id,
            airport_code=airport.airport_code
        )

    if not updated_airport:
        raise HTTPException(status_code=404, detail="Airport not found or failed to update")

    return updated_airport


@router.delete("/airport/{id}")
async def delete_airport(id: int):
    airport_repo = AirportRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await airport_repo.check_connection(session=session)
        deleted_airport = await airport_repo.delete_airport(session=session, airport_id=id)

    if not deleted_airport:
        raise HTTPException(status_code=404, detail="Airport not found or failed to delete")

    return {"message": "Airport deleted successfully"}


@router.post("/staff", response_model=StaffSchema)
async def create_staff(staff: StaffSchema) -> StaffSchema:
    staff_repo = StaffRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await staff_repo.check_connection(session=session)
        new_staff = await staff_repo.create_staff(
            session=session,
            first_name=staff.first_name,
            second_name=staff.second_name,
            airline_id=staff.airline_id,
            experience=staff.experience
        )

    return new_staff


@router.get("/staff/{id}", response_model=StaffSchema)
async def get_staff(id: int) -> StaffSchema:
    staff_repo = StaffRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await staff_repo.check_connection(session=session)
        staff = await staff_repo.get_staff(session=session, employee_id=id)

    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")

    return staff


@router.put("/staff/{id}", response_model=StaffSchema)
async def update_staff(id: int, staff: StaffSchema) -> StaffSchema:
    staff_repo = StaffRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await staff_repo.check_connection(session=session)
        updated_staff = await staff_repo.update_staff(
            session=session,
            employee_id=id,
            first_name=staff.first_name,
            second_name=staff.second_name,
            airline_id=staff.airline_id,
            experience=staff.experience
        )

    if not updated_staff:
        raise HTTPException(status_code=404, detail="Staff not found or failed to update")

    return updated_staff


@router.delete("/staff/{id}")
async def delete_staff(id: int):
    staff_repo = StaffRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await staff_repo.check_connection(session=session)
        deleted_staff = await staff_repo.delete_staff(session=session, employee_id=id)

    if not deleted_staff:
        raise HTTPException(status_code=404, detail="Staff not found or failed to delete")

    return {"message": "Staff deleted successfully"}



@router.post("/crew", response_model=CrewSchema)
async def create_crew(crew: CrewSchema) -> CrewSchema:
    crew_repo = CrewRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await crew_repo.check_connection(session=session)
        new_crew = await crew_repo.create_crew(
            session=session,
            pilot1=crew.pilot1,
            pilot2=crew.pilot2,
            stewardess=crew.stewardess
        )

    return new_crew


@router.get("/crew/{id}", response_model=CrewSchema)
async def get_crew(id: int) -> CrewSchema:
    crew_repo = CrewRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await crew_repo.check_connection(session=session)
        crew = await crew_repo.get_crew(session=session, crew_id=id)

    if not crew:
        raise HTTPException(status_code=404, detail="Crew not found")

    return crew


@router.put("/crew/{id}", response_model=CrewSchema)
async def update_crew(id: int, crew: CrewSchema) -> CrewSchema:
    crew_repo = CrewRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await crew_repo.check_connection(session=session)
        updated_crew = await crew_repo.update_crew(
            session=session,
            crew_id=id,
            pilot1=crew.pilot1,
            pilot2=crew.pilot2,
            stewardess=crew.stewardess
        )

    if not updated_crew:
        raise HTTPException(status_code=404, detail="Crew not found or failed to update")

    return updated_crew


@router.delete("/crew/{id}")
async def delete_crew(id: int):
    crew_repo = CrewRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await crew_repo.check_connection(session=session)
        deleted_crew = await crew_repo.delete_crew(session=session, crew_id=id)

    if not deleted_crew:
        raise HTTPException(status_code=404, detail="Crew not found or failed to delete")

    return {"message": "Crew deleted successfully"}



@router.post("/route", response_model=RouteSchema)
async def create_route(route: RouteSchema) -> RouteSchema:
    route_repo = RouteRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await route_repo.check_connection(session=session)
        new_route = await route_repo.create_route(
            session=session,
            departure_airport_id=route.departure_airport_id,
            arrival_airport_id=route.arrival_airport_id,
            distance=route.distance,
            flight_time=route.flight_time
        )

    return new_route


@router.get("/route/{id}", response_model=RouteSchema)
async def get_route(id: int) -> RouteSchema:
    route_repo = RouteRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await route_repo.check_connection(session=session)
        route = await route_repo.get_route(session=session, route_id=id)

    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    return route


@router.put("/route/{id}", response_model=RouteSchema)
async def update_route(id: int, route: RouteSchema) -> RouteSchema:
    route_repo = RouteRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await route_repo.check_connection(session=session)
        updated_route = await route_repo.update_route(
            session=session,
            route_id=id,
            departure_airport_id=route.departure_airport_id,
            arrival_airport_id=route.arrival_airport_id,
            distance=route.distance,
            flight_time=route.flight_time
        )

    if not updated_route:
        raise HTTPException(status_code=404, detail="Route not found or failed to update")

    return updated_route


@router.delete("/route/{id}")
async def delete_route(id: int):
    route_repo = RouteRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await route_repo.check_connection(session=session)
        deleted_route = await route_repo.delete_route(session=session, route_id=id)

    if not deleted_route:
        raise HTTPException(status_code=404, detail="Route not found or failed to delete")

    return {"message": "Route deleted successfully"}



@router.post("/flight", response_model=FlightSchema)
async def create_flight(flight: FlightSchema) -> FlightSchema:
    flight_repo = FlightRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await flight_repo.check_connection(session=session)
        new_flight = await flight_repo.create_flight(
            session=session,
            route_id=flight.route_id,
            plane_id=flight.plane_id,
            crew_id=flight.crew_id,
            airline_id=flight.airline_id,
            departure_time=flight.departure_time,
            arrival_time=flight.arrival_time
        )

    return new_flight


@router.get("/flight/{id}", response_model=FlightSchema)
async def get_flight(id: int) -> FlightSchema:
    flight_repo = FlightRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await flight_repo.check_connection(session=session)
        flight = await flight_repo.get_flight(session=session, flight_id=id)

    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    return flight


@router.put("/flight/{id}", response_model=FlightSchema)
async def update_flight(id: int, flight: FlightSchema) -> FlightSchema:
    flight_repo = FlightRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await flight_repo.check_connection(session=session)
        updated_flight = await flight_repo.update_flight(
            session=session,
            flight_id=id,
            route_id=flight.route_id,
            plane_id=flight.plane_id,
            crew_id=flight.crew_id,
            airline_id=flight.airline_id,
            departure_time=flight.departure_time,
            arrival_time=flight.arrival_time
        )

    if not updated_flight:
        raise HTTPException(status_code=404, detail="Flight not found or failed to update")

    return updated_flight


@router.delete("/flight/{id}")
async def delete_flight(id: int):
    flight_repo = FlightRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await flight_repo.check_connection(session=session)
        deleted_flight = await flight_repo.delete_flight(session=session, flight_id=id)

    if not deleted_flight:
        raise HTTPException(status_code=404, detail="Flight not found or failed to delete")

    return {"message": "Flight deleted successfully"}



@router.post("/ticket", response_model=TicketSchema)
async def create_ticket(ticket: TicketSchema) -> TicketSchema:
    ticket_repo = TicketRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await ticket_repo.check_connection(session=session)
        new_ticket = await ticket_repo.create_ticket(
            session=session,
            customer_id=ticket.customer_id,
            date_of_purchase=ticket.date_of_purchase,
            price=ticket.price,
            flight_id=ticket.flight_id
        )

    return new_ticket


@router.get("/ticket/{id}", response_model=TicketSchema)
async def get_ticket(id: int) -> TicketSchema:
    ticket_repo = TicketRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await ticket_repo.check_connection(session=session)
        ticket = await ticket_repo.get_ticket(session=session, ticket_id=id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket


@router.put("/ticket/{id}", response_model=TicketSchema)
async def update_ticket(id: int, ticket: TicketSchema) -> TicketSchema:
    ticket_repo = TicketRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await ticket_repo.check_connection(session=session)
        updated_ticket = await ticket_repo.update_ticket(
            session=session,
            ticket_id=id,
            customer_id=ticket.customer_id,
            date_of_purchase=ticket.date_of_purchase,
            price=ticket.price,
            flight_id=ticket.flight_id
        )

    if not updated_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found or failed to update")

    return updated_ticket


@router.delete("/ticket/{id}")
async def delete_ticket(id: int):
    ticket_repo = TicketRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await ticket_repo.check_connection(session=session)
        deleted_ticket = await ticket_repo.delete_ticket(session=session, ticket_id=id)

    if not deleted_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found or failed to delete")

    return {"message": "Ticket deleted successfully"}
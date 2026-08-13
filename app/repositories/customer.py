from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import engine
from app.models import Customer


def get_all_customers():
    with Session(engine) as session:
        statement = select(Customer)

        customers = session.scalars(statement).all()

        return [
            {
                "id": customer.id,
                "name": customer.name,
                "email": customer.email,
                "city": customer.city,
            }
            for customer in customers
        ]
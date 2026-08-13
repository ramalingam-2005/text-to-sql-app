from sqlalchemy import text
from app.database import engine
def get_customers():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT * FROM customers")
        )

        customers = []

        for row in result:
            customers.append(dict(row._mapping))

        return customers
    
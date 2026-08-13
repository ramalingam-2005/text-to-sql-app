from fastapi import FastAPI
from sqlalchemy import text


from app.repositories.customer import get_all_customers

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Text-to-SQL API is running"}


@app.get("/customers")
def get_customers():
    return get_all_customers()
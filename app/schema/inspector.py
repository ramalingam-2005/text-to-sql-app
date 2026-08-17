from sqlalchemy import inspect

from app.database import engine


def get_database_schema():
    inspector = inspect(engine)

    schema = {}

    tables = inspector.get_table_names()

    for table in tables:
        columns = inspector.get_columns(table)

        primary_key = inspector.get_pk_constraint(table)

        foreign_keys = inspector.get_foreign_keys(table)

        schema[table] = {
            "columns": [
                {
                    "name": column["name"],
                    "type": str(column["type"]),
                    "nullable": column["nullable"],
                }
                for column in columns
            ],
            "primary_key": primary_key["constrained_columns"],
            "foreign_keys": [
                {
                    "columns": foreign_key["constrained_columns"],
                    "referred_table": foreign_key["referred_table"],
                    "referred_columns": foreign_key["referred_columns"],
                }
                for foreign_key in foreign_keys
            ],
        }

    return schema


if __name__ == "__main__":
    schema = get_database_schema()

    for table, information in schema.items():
        print(f"\n{table}")
        print(information)
from sqlalchemy import text

from app.database import engine
from app.sql.validator import validate_sql


def execute_sql(sql):

    is_valid, validated_sql = validate_sql(sql)

    if not is_valid:
        raise ValueError(validated_sql)

    with engine.connect() as connection:

        result = connection.execute(
            text(validated_sql)
        )

        rows = result.mappings().all()

    return rows
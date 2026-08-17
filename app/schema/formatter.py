from app.schema.inspector import get_database_schema


def format_table_schema(table_name, table_info):
    lines = []

    lines.append(f"Table: {table_name}")
    lines.append("")
    lines.append("Columns:")

    for column in table_info["columns"]:
        nullable = "NULL" if column["nullable"] else "NOT NULL"

        lines.append(
            f"- {column['name']}: {column['type']} ({nullable})"
        )

    lines.append("")
    lines.append("Primary Key:")

    for column in table_info["primary_key"]:
        lines.append(f"- {column}")

    lines.append("")
    lines.append("Relationships:")

    if table_info["foreign_keys"]:
        for foreign_key in table_info["foreign_keys"]:
            columns = ", ".join(foreign_key["columns"])
            referred_columns = ", ".join(
                foreign_key["referred_columns"]
            )

            lines.append(
                f"- {columns} references "
                f"{foreign_key['referred_table']}"
                f"({referred_columns})"
            )
    else:
        lines.append("- None")

    return "\n".join(lines)


def build_schema_documents():
    schema = get_database_schema()

    documents = []

    for table_name, table_info in schema.items():
        document = format_table_schema(
            table_name,
            table_info
        )

        documents.append({
            "table": table_name,
            "content": document
        })

    return documents


if __name__ == "__main__":
    documents = build_schema_documents()

    for document in documents:
        print("=" * 60)
        print(document["content"])
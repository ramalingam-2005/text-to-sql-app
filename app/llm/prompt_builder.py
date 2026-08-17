from app.vectorstore.retriever import retrieve_schema


def build_sql_prompt(question, schema_documents):
    schema_text = "\n\n".join(
        document["content"]
        for document in schema_documents
    )

    prompt = f"""
You are an expert SQL query generator.

Your task is to convert the user's natural language question
into a valid MySQL SQL query.

Use ONLY the tables and columns provided in the database schema.

Database Schema:
----------------
{schema_text}
----------------

User Question:
{question}

Rules:
1. Generate only valid MySQL SQL.
2. Use only tables and columns from the provided schema.
3. Do not invent tables or columns.
4. Use appropriate JOIN conditions based on foreign keys.
5. Do not modify the database.
6. Do not use INSERT, UPDATE, DELETE, DROP, ALTER, or TRUNCATE.
7. Return only the SQL query.
"""

    return prompt


if __name__ == "__main__":

    question = "Which customers placed orders?"

    results = retrieve_schema(
        question,
        top_k=3
    )

    schema_documents = []

    for document, metadata in zip(
        results["documents"][0],
        results["metadatas"][0]
    ):
        schema_documents.append({
            "table": metadata["table"],
            "content": document
        })

    prompt = build_sql_prompt(
        question,
        schema_documents
    )

    print(prompt)